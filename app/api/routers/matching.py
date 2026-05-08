import asyncio
import logging
import math
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.concurrency import run_in_threadpool

from app.aldi.client import AldiClient
from app.api.dependencies import (
    get_aldi_client,
    get_kroger_client,
    get_publix_client,
    get_walmart_client,
)
from app.kroger.client import KrogerClient
from app.errors import ScraperBlockedError, ScraperNetworkError, ScraperParsingError
from app.matching.models import MatchSearchRequest, MatchSearchResponse
from app.matching.normalizer import fingerprint_query, normalize_text
from app.matching.service import SUPPORTED_RETAILERS, match_products
from app.publix.client import PublixClient
from app.walmart.client import WalmartClient

router = APIRouter()
logger = logging.getLogger(__name__)


def _selected_retailers(request: MatchSearchRequest) -> list[str]:
    selected = request.retailers or list(SUPPORTED_RETAILERS)
    normalized = [retailer.lower() for retailer in selected]
    unsupported = sorted(set(normalized) - set(SUPPORTED_RETAILERS))
    if unsupported:
        raise HTTPException(status_code=422, detail=f"Unsupported retailers: {', '.join(unsupported)}")
    return normalized


def _add_variant(variants: list[str], value: str | None):
    if not value:
        return
    normalized = " ".join(value.split())
    if normalized and normalized.lower() not in {variant.lower() for variant in variants}:
        variants.append(normalized)


def _size_variant(query_fingerprint) -> str | None:
    size = query_fingerprint.size
    if not size:
        return None

    if size.unit == "fl_oz" and math.isclose(size.value, 128.0):
        return "1 gallon"
    if size.unit == "fl_oz" and math.isclose(size.value, 64.0):
        return "half gallon"
    if size.unit == "ct":
        return f"{size.value:g} ct"
    return f"{size.value:g} {size.unit}"


def _query_variants(query: str) -> list[str]:
    variants = [query]
    normalized = normalize_text(query)
    if normalized != query.lower().strip():
        _add_variant(variants, normalized)

    query_fingerprint = fingerprint_query(query)
    if query_fingerprint.category == "milk":
        fat_level = query_fingerprint.attributes.get("fat_level")
        size = _size_variant(query_fingerprint)
        if fat_level and size:
            _add_variant(variants, f"{fat_level} milk {size}")
            _add_variant(variants, f"milk {size}")
        elif fat_level:
            _add_variant(variants, f"{fat_level} milk")

    return variants[:3]


def _public_error_code(error: Exception) -> str:
    message = str(error).lower()
    if "browser" in message and "executable doesn't exist" in message:
        return "browser_runtime_unavailable"
    if isinstance(error, ScraperBlockedError):
        return "retailer_blocked"
    if isinstance(error, ScraperNetworkError):
        return "network_error"
    if isinstance(error, ScraperParsingError):
        return "parsing_error"
    return "unknown_error"


def _search_retailer(
    retailer: str,
    client: Any,
    request: MatchSearchRequest,
    location_ids: dict[str, str],
) -> list[dict[str, Any]]:
    location_id = location_ids.get(retailer)
    kwargs: dict[str, Any] = {}
    variants = _query_variants(request.query)
    per_variant_results = max(
        8,
        math.ceil(request.max_candidates_per_retailer / len(variants)),
    )

    if location_id:
        cookies = client.build_cookies(location_id, request.zip_code or "")
        if cookies is not None:
            kwargs["cookies"] = cookies

    if retailer == "aldi" and request.zip_code:
        kwargs["zip_code"] = request.zip_code

    products = []
    for query in variants:
        products.extend(client.search_products(
            query=query,
            location_id=location_id,
            max_results=per_variant_results,
            **kwargs,
        ) or [])
    return products


@router.post("/search", response_model=MatchSearchResponse)
async def match_search(
    request: MatchSearchRequest,
    aldi_location_id: str | None = Query(None, description="aldi store location id"),
    kroger_location_id: str | None = Query(None, description="kroger store location id"),
    publix_location_id: str | None = Query(None, description="publix store location id"),
    walmart_location_id: str | None = Query(None, description="walmart store location id"),
    aldi_client: AldiClient = Depends(get_aldi_client),
    kroger_client: KrogerClient = Depends(get_kroger_client),
    publix_client: PublixClient = Depends(get_publix_client),
    walmart_client: WalmartClient = Depends(get_walmart_client),
):
    clients = {
        "aldi": aldi_client,
        "kroger": kroger_client,
        "publix": publix_client,
        "walmart": walmart_client,
    }
    retailers = _selected_retailers(request)
    location_ids = {
        retailer: location_id
        for retailer, location_id in {
            "aldi": aldi_location_id,
            "kroger": kroger_location_id,
            "publix": publix_location_id,
            "walmart": walmart_location_id,
        }.items()
        if location_id
    }

    tasks = {
        retailer: run_in_threadpool(_search_retailer, retailer, clients[retailer], request, location_ids)
        for retailer in retailers
    }
    gathered = await asyncio.gather(*tasks.values(), return_exceptions=True)

    products = []
    errors = {}
    for retailer, result in zip(tasks.keys(), gathered):
        if isinstance(result, Exception):
            logger.error(
                "Error in match search for %s",
                retailer,
                exc_info=(type(result), result, result.__traceback__),
            )
            errors[retailer] = _public_error_code(result)
            continue
        products.extend(result or [])

    return match_products(
        request.query,
        products,
        retailers=retailers,
        max_candidates_per_retailer=request.max_candidates_per_retailer,
        equivalence_threshold=request.equivalence_threshold,
        errors=errors,
    )
