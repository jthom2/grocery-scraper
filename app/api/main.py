from typing import List, Optional
import logging
from fastapi import FastAPI, Query, HTTPException

from app.models import NormalizedProduct
from app.aldi.client import AldiClient
from app.kroger.client import KrogerClient
from app.publix.client import PublixClient
from app.walmart.client import WalmartClient

# setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Grocery Scraper API",
    description="API for scraping products from major grocery retailers.",
    version="0.1.0"
)

# global singletons
aldi_client = AldiClient()
kroger_client = KrogerClient()
publix_client = PublixClient()
walmart_client = WalmartClient()


@app.get("/api/v1/aldi/search", response_model=List[NormalizedProduct])
def search_aldi(
    q: str = Query(..., description="search query"),
    location_id: Optional[str] = Query(None, description="store location id"),
    zip_code: Optional[str] = Query(None, description="zip code for location-specific pricing"),
    max_results: int = Query(5, ge=1, le=50, description="maximum number of results")
):
    try:
        # aldi uses zip_code in search_products for cache isolation
        return aldi_client.search_products(
            query=q, 
            location_id=location_id, 
            max_results=max_results, 
            zip_code=zip_code
        )
    except Exception as e:
        logger.exception("Aldi search failed")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/v1/kroger/search", response_model=List[NormalizedProduct])
def search_kroger(
    q: str = Query(..., description="search query"),
    location_id: Optional[str] = Query(None, description="store location id"),
    zip_code: Optional[str] = Query(None, description="zip code to find closest store"),
    max_results: int = Query(5, ge=1, le=50, description="maximum number of results")
):
    try:
        resolved_location_id = location_id
        cookies = None
        if not resolved_location_id and zip_code:
            stores = kroger_client.get_stores(zip_code)
            if stores:
                resolved_location_id = stores[0]['location_id']
        
        if resolved_location_id:
            cookies = kroger_client._build_cookies(resolved_location_id, zip_code)

        return kroger_client.search_products(
            query=q, 
            location_id=resolved_location_id, 
            max_results=max_results,
            cookies=cookies
        )
    except Exception as e:
        logger.exception("Kroger search failed")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/v1/publix/search", response_model=List[NormalizedProduct])
def search_publix(
    q: str = Query(..., description="search query"),
    location_id: Optional[str] = Query(None, description="store location id"),
    zip_code: Optional[str] = Query(None, description="zip code to find closest store"),
    max_results: int = Query(5, ge=1, le=50, description="maximum number of results")
):
    try:
        resolved_location_id = location_id
        if not resolved_location_id and zip_code:
            stores = publix_client.get_stores(zip_code)
            if stores:
                resolved_location_id = stores[0]['location_id']

        return publix_client.search_products(
            query=q, 
            location_id=resolved_location_id, 
            max_results=max_results
        )
    except Exception as e:
        logger.exception("Publix search failed")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/v1/walmart/search", response_model=List[NormalizedProduct])
def search_walmart(
    q: str = Query(..., description="search query"),
    location_id: Optional[str] = Query(None, description="store location id"),
    zip_code: Optional[str] = Query(None, description="zip code to find closest store"),
    max_results: int = Query(5, ge=1, le=50, description="maximum number of results")
):
    try:
        resolved_location_id = location_id
        cookies = None
        if not resolved_location_id and zip_code:
            stores = walmart_client.get_stores(zip_code)
            if stores:
                resolved_location_id = stores[0]['location_id']

        if resolved_location_id:
            cookies = walmart_client._build_cookies(resolved_location_id, zip_code)

        return walmart_client.search_products(
            query=q, 
            location_id=resolved_location_id, 
            max_results=max_results,
            cookies=cookies
        )
    except Exception as e:
        logger.exception("Walmart search failed")
        raise HTTPException(status_code=500, detail=str(e))


def start():
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)


if __name__ == "__main__":
    start()
