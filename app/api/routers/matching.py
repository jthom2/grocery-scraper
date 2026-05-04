import asyncio
import logging
from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from fastapi.concurrency import run_in_threadpool

from app.aldi.client import AldiClient
from app.api.dependencies import (
    get_aldi_client,
    get_kroger_client,
    get_publix_client,
    get_walmart_client,
)
from app.kroger.client import KrogerClient
from app.matching.models import MatchSearchRequest, MatchSearchResponse
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


def _search_retailer(retailer: str, client: Any, request: MatchSearchRequest) -> list[dict[str, Any]]:
    location_id = request.location_ids.get(retailer)
    kwargs: dict[str, Any] = {}

    if location_id:
        cookies = client.build_cookies(location_id, request.zip_code or "")
        if cookies is not None:
            kwargs["cookies"] = cookies

    if retailer == "aldi" and request.zip_code:
        kwargs["zip_code"] = request.zip_code

    return client.search_products(
        query=request.query,
        location_id=location_id,
        max_results=request.max_candidates_per_retailer,
        **kwargs,
    )


@router.post("/search", response_model=MatchSearchResponse)
async def match_search(
    request: MatchSearchRequest,
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

    tasks = {
        retailer: run_in_threadpool(_search_retailer, retailer, clients[retailer], request)
        for retailer in retailers
    }
    gathered = await asyncio.gather(*tasks.values(), return_exceptions=True)

    products = []
    errors = {}
    for retailer, result in zip(tasks.keys(), gathered):
        if isinstance(result, Exception):
            logger.error("Error in match search for %s: %s", retailer, result)
            errors[retailer] = str(result)
            continue
        products.extend(result or [])

    return match_products(
        request.query,
        products,
        equivalence_threshold=request.equivalence_threshold,
        errors=errors,
    )
