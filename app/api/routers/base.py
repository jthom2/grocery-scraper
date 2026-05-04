from typing import List, Optional, Callable
from fastapi import APIRouter, Depends, Query
from fastapi.concurrency import run_in_threadpool

from app.models import NormalizedProduct, NormalizedLocation
from app.utils.store_client import BaseStoreClient

def create_store_router(client_dependency: Callable[..., BaseStoreClient]) -> APIRouter:
    router = APIRouter()

    @router.get("/locations", response_model=List[NormalizedLocation])
    async def get_locations(
        zip_code: str = Query(..., description="zip code to find stores near"),
        max_results: int = Query(10, ge=1, le=50),
        client: BaseStoreClient = Depends(client_dependency)
    ):
        return await run_in_threadpool(client.get_stores, zip_code, max_results=max_results)

    @router.get("/search", response_model=List[NormalizedProduct])
    async def search(
        q: str = Query(..., description="search query"),
        location_id: Optional[str] = Query(None, description="store location id"),
        max_results: int = Query(5, ge=1, le=50, description="maximum number of results"),
        client: BaseStoreClient = Depends(client_dependency)
    ):
        def _search_with_cookies():
            cookies = None
            if location_id:
                cookies = client.build_cookies(location_id, "")
            return client.search_products(
                query=q, 
                location_id=location_id, 
                max_results=max_results,
                cookies=cookies
            )

        return await run_in_threadpool(_search_with_cookies)

    return router
