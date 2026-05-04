from app.api.dependencies import get_walmart_client
from app.api.routers.base import create_store_router

router = create_store_router(get_walmart_client)
