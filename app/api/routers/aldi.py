from typing import List, Optional
from fastapi import APIRouter, Depends, Query, HTTPException
from fastapi.concurrency import run_in_threadpool

from app.models import NormalizedProduct, NormalizedLocation
from app.aldi.client import AldiClient
from app.api.dependencies import get_aldi_client

router = APIRouter()

@router.get("/locations", response_model=List[NormalizedLocation])
async def get_aldi_locations(
    zip_code: str = Query(..., description="zip code to find stores near"),
    max_results: int = Query(10, ge=1, le=50),
    client: AldiClient = Depends(get_aldi_client)
):
    return await run_in_threadpool(client.get_stores, zip_code, max_results=max_results)

@router.get("/search", response_model=List[NormalizedProduct])
async def search_aldi(
    q: str = Query(..., description="search query"),
    location_id: Optional[str] = Query(None, description="store location id"),
    max_results: int = Query(5, ge=1, le=50, description="maximum number of results"),
    client: AldiClient = Depends(get_aldi_client)
):
    return await run_in_threadpool(
        client.search_products,
        query=q, 
        location_id=location_id, 
        max_results=max_results
    )
