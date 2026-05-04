import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.errors import ScraperError
from app.api.exceptions import scraper_exception_handler, generic_exception_handler
from app.api.routers import aldi, kroger, matching, publix, walmart, unified

# setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Grocery Scraper API",
    description="API for scraping products from major grocery retailers.",
    version="0.1.0"
)

# middleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # adjust for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# exception handlers

app.add_exception_handler(ScraperError, scraper_exception_handler)
app.add_exception_handler(Exception, generic_exception_handler)

# routers

app.include_router(aldi.router, prefix="/api/v1/aldi", tags=["aldi"])
app.include_router(kroger.router, prefix="/api/v1/kroger", tags=["kroger"])
app.include_router(publix.router, prefix="/api/v1/publix", tags=["publix"])
app.include_router(walmart.router, prefix="/api/v1/walmart", tags=["walmart"])
app.include_router(unified.router, prefix="/api/v1", tags=["unified"])
app.include_router(matching.router, prefix="/api/v1/match", tags=["matching"])

# system endpoints

@app.get("/health", tags=["system"])
async def health_check():
    return {"status": "ok"}

def start():
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

if __name__ == "__main__":
    start()
