from typing import List, Optional
import logging
import asyncio
from fastapi import FastAPI, Query, HTTPException

from app.models import NormalizedProduct, NormalizedLocation
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


# --- Store Locators ---

@app.get("/api/v1/aldi/locations", response_model=List[NormalizedLocation])
def get_aldi_locations(
    zip_code: str = Query(..., description="zip code to find stores near"),
    max_results: int = Query(10, ge=1, le=50)
):
    try:
        return aldi_client.get_stores(zip_code, max_results=max_results)
    except Exception as e:
        logger.exception("Aldi store lookup failed")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/v1/kroger/locations", response_model=List[NormalizedLocation])
def get_kroger_locations(
    zip_code: str = Query(..., description="zip code to find stores near"),
    max_results: int = Query(10, ge=1, le=50)
):
    try:
        return kroger_client.get_stores(zip_code, max_results=max_results)
    except Exception as e:
        logger.exception("Kroger store lookup failed")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/v1/publix/locations", response_model=List[NormalizedLocation])
def get_publix_locations(
    zip_code: str = Query(..., description="zip code to find stores near"),
    max_results: int = Query(10, ge=1, le=50)
):
    try:
        return publix_client.get_stores(zip_code, max_results=max_results)
    except Exception as e:
        logger.exception("Publix store lookup failed")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/v1/walmart/locations", response_model=List[NormalizedLocation])
def get_walmart_locations(
    zip_code: str = Query(..., description="zip code to find stores near"),
    max_results: int = Query(10, ge=1, le=50)
):
    try:
        return walmart_client.get_stores(zip_code, max_results=max_results)
    except Exception as e:
        logger.exception("Walmart store lookup failed")
        raise HTTPException(status_code=500, detail=str(e))


# --- Search Endpoints ---

@app.get("/api/v1/aldi/search", response_model=List[NormalizedProduct])
def search_aldi(
    q: str = Query(..., description="search query"),
    location_id: Optional[str] = Query(None, description="store location id"),
    max_results: int = Query(5, ge=1, le=50, description="maximum number of results")
):
    try:
        return aldi_client.search_products(
            query=q, 
            location_id=location_id, 
            max_results=max_results
        )
    except Exception as e:
        logger.exception("Aldi search failed")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/v1/kroger/search", response_model=List[NormalizedProduct])
def search_kroger(
    q: str = Query(..., description="search query"),
    location_id: Optional[str] = Query(None, description="store location id"),
    max_results: int = Query(5, ge=1, le=50, description="maximum number of results")
):
    try:
        cookies = None
        if location_id:
            cookies = kroger_client._build_cookies(location_id, None)

        return kroger_client.search_products(
            query=q, 
            location_id=location_id, 
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
    max_results: int = Query(5, ge=1, le=50, description="maximum number of results")
):
    try:
        return publix_client.search_products(
            query=q, 
            location_id=location_id, 
            max_results=max_results
        )
    except Exception as e:
        logger.exception("Publix search failed")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/v1/walmart/search", response_model=List[NormalizedProduct])
def search_walmart(
    q: str = Query(..., description="search query"),
    location_id: Optional[str] = Query(None, description="store location id"),
    max_results: int = Query(5, ge=1, le=50, description="maximum number of results")
):
    try:
        cookies = None
        if location_id:
            cookies = walmart_client._build_cookies(location_id, None)

        return walmart_client.search_products(
            query=q, 
            location_id=location_id, 
            max_results=max_results,
            cookies=cookies
        )
    except Exception as e:
        logger.exception("Walmart search failed")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/v1/search", response_model=List[NormalizedProduct])
async def search_all(
    q: str = Query(..., description="search query"),
    aldi_location_id: Optional[str] = Query(None, description="aldi store location id"),
    kroger_location_id: Optional[str] = Query(None, description="kroger store location id"),
    publix_location_id: Optional[str] = Query(None, description="publix store location id"),
    walmart_location_id: Optional[str] = Query(None, description="walmart store location id"),
    max_results: int = Query(5, ge=1, le=50, description="maximum number of results per store")
):
    tasks = [
        asyncio.to_thread(search_aldi, q, aldi_location_id, max_results),
        asyncio.to_thread(search_kroger, q, kroger_location_id, max_results),
        asyncio.to_thread(search_publix, q, publix_location_id, max_results),
        asyncio.to_thread(search_walmart, q, walmart_location_id, max_results),
    ]
    
    results = await asyncio.gather(*tasks, return_exceptions=True)
    
    final_results = []
    for res in results:
        if isinstance(res, Exception):
            logger.error(f"Error in unified search: {res}")
        elif res:
            final_results.extend(res)
            
    return final_results


def start():
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)


if __name__ == "__main__":
    start()
