import os
try:
    import orjson
except ImportError:
    import json as orjson
import redis
from typing import Any


# Deep module for caching store location data in Redis.
# Encapsulates connection management, JSON serialization, and key formatting.
class StoreCache:
    def __init__(self, host: str = "localhost", port: int = 6379, db: int = 0):
        self.host = host
        self.port = port
        self.db = db
        self._client = None
        self._is_available = True

    # returns a singleton redis client instance or None if connection fails
    @property
    def client(self) -> redis.Redis | None:
        if not self._is_available:
            return None
            
        if self._client is None:
            try:
                self._client = redis.Redis(
                    host=self.host, 
                    port=self.port, 
                    db=self.db, 
                    socket_timeout=2, 
                    decode_responses=True
                )
                self._client.ping()
            except (redis.ConnectionError, redis.TimeoutError):
                # graceful degradation if redis is not running
                self._is_available = False
                self._client = None
        return self._client

    # formats the cache key to prevent collision across retailers
    def _get_key(self, retailer: str, zip_code: str) -> str:
        # ensuring zip_code is stripped and consistent
        z = zip_code.strip() if zip_code else "unknown"
        return f"stores:{retailer}:{z}"

    # retrieves cached stores for a specific retailer and zip code
    def get(self, retailer: str, zip_code: str) -> list[dict[str, Any]] | None:
        if not (client := self.client):
            return None

        key = self._get_key(retailer, zip_code)
        try:
            if data := client.get(key):
                return orjson.loads(data)
        except Exception:
            # log or handle deserialization error
            return None
        return None

    # stores normalized location data with a time-to-live (TTL)
    def set(self, retailer: str, zip_code: str, stores: list[dict[str, Any]], ttl_hours: int = 168):
        if not (client := self.client):
            return

        key = self._get_key(retailer, zip_code)
        try:
            serialized = orjson.dumps(stores)
            client.setex(key, ttl_hours * 3600, serialized)
        except Exception:
            # log or handle serialization error
            pass


# global singleton instance for the application
store_cache = StoreCache(
    host=os.getenv("REDIS_HOST", "localhost"),
    port=int(os.getenv("REDIS_PORT", 6379)),
)
