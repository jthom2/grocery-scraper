import asyncio
import logging
from typing import List, Optional
from fastapi import APIRouter, Depends, Query
from fastapi.concurrency import run_in_threadpool

from app.models import NormalizedProduct, StoreLocationsResponse
from app.aldi.client import AldiClient
from app.kroger.client import KrogerClient
from app.publix.client import PublixClient
from app.walmart.client import WalmartClient
from app.api.dependencies import (
    get_aldi_client, get_kroger_client, get_publix_client, get_walmart_client
)

router = APIRouter()
logger = logging.getLogger(__name__)


@router.get("/locations", response_model=StoreLocationsResponse)
async def get_locations_all(
    zip_code: str = Query(..., description="zip code to find stores near"),
    max_results_per_retailer: int = Query(
        10,
        ge=1,
        le=50,
        description="maximum number of store locations per retailer",
    ),
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

    tasks = {
        retailer: run_in_threadpool(
            client.get_stores,
            zip_code,
            max_results=max_results_per_retailer,
        )
        for retailer, client in clients.items()
    }
    gathered = await asyncio.gather(*tasks.values(), return_exceptions=True)

    locations = {}
    errors = {}
    for retailer, result in zip(tasks.keys(), gathered):
        if isinstance(result, Exception):
            logger.error("Error in unified locations for %s: %s", retailer, result)
            locations[retailer] = []
            errors[retailer] = str(result)
            continue
        locations[retailer] = result or []

    return {
        "zip_code": zip_code,
        "locations": locations,
        "errors": errors,
    }


@router.get("/search", response_model=List[NormalizedProduct])
async def search_all(
    q: str = Query(..., description="search query"),
    aldi_location_id: Optional[str] = Query(None, description="aldi store location id"),
    kroger_location_id: Optional[str] = Query(None, description="kroger store location id"),
    publix_location_id: Optional[str] = Query(None, description="publix store location id"),
    walmart_location_id: Optional[str] = Query(None, description="walmart store location id"),
    aldi_client: AldiClient = Depends(get_aldi_client),
    kroger_client: KrogerClient = Depends(get_kroger_client),
    publix_client: PublixClient = Depends(get_publix_client),
    walmart_client: WalmartClient = Depends(get_walmart_client),
):
    # helper functions to wrap the client calls
    def fetch_aldi():
        return aldi_client.search_products(q, aldi_location_id, max_results=1)

    def fetch_kroger():
        cookies = kroger_client.build_cookies(kroger_location_id, None) if kroger_location_id else None
        return kroger_client.search_products(q, kroger_location_id, max_results=1, cookies=cookies)

    def fetch_publix():
        return publix_client.search_products(q, publix_location_id, max_results=1)

    def fetch_walmart():
        cookies = walmart_client.build_cookies(walmart_location_id, None) if walmart_location_id else None
        return walmart_client.search_products(q, walmart_location_id, max_results=1, cookies=cookies)

    tasks = [
        run_in_threadpool(fetch_aldi),
        run_in_threadpool(fetch_kroger),
        run_in_threadpool(fetch_publix),
        run_in_threadpool(fetch_walmart),
    ]
    
    results = await asyncio.gather(*tasks, return_exceptions=True)
    
    final_results = []
    for res in results:
        if isinstance(res, Exception):
            logger.error(f"Error in unified search: {res}")
        elif res:
            # take only the first result from each store as per original logic
            final_results.extend(res[:1])
            
    return final_results
