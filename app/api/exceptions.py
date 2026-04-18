import logging
from fastapi import Request, status
from fastapi.responses import JSONResponse
from app.errors import ScraperError

logger = logging.getLogger(__name__)

async def scraper_exception_handler(request: Request, exc: ScraperError):
    # handle all scraper-related errors with a standardized response
    logger.error(f"Scraper error occurred: {exc.message} (URL: {exc.url}, Status: {exc.status_code})")
    
    # map internal status codes or types to HTTP status codes if needed
    # for now, we'll use 500 or the status_code from the exception
    status_code = exc.status_code or status.HTTP_500_INTERNAL_SERVER_ERROR
    
    return JSONResponse(
        status_code=status_code,
        content={"detail": "An error occurred while fetching data from the retailer. Please try again later."},
    )

async def generic_exception_handler(request: Request, exc: Exception):
    # handle all unhandled exceptions to prevent leaking stack traces
    logger.exception("An unhandled exception occurred")
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "An internal server error occurred. Our team has been notified."},
    )
