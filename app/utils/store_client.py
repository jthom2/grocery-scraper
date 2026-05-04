from abc import ABC, abstractmethod
from typing import Any

from app.utils.store_cache import store_cache
from app.utils.product_cache import product_cache


class BaseStoreClient(ABC):
    # template method base for all retailer clients.
    # owns cache-aside logic, CLI interaction, and display delegation.
    # subclasses implement _fetch_stores and _fetch_products for retailer-specific network calls.

    @property
    @abstractmethod
    def retailer_name(self) -> str:
        ...

    @abstractmethod
    def _fetch_stores(self, zip_code: str, max_results: int = 10) -> list[dict[str, Any]]:
        # network fetch + normalization only. no caching.
        ...

    @abstractmethod
    def _fetch_products(self, query: str, location_id: str | None = None, max_results: int = 5, **kwargs) -> list[dict[str, Any]]:
        # network fetch + normalization only. no caching.
        ...

    # --- optional hooks (override when needed) ---

    def filter_stores(self, stores: list[dict[str, Any]]) -> list[dict[str, Any]]:
        # identity by default; kroger overrides to filter by brand
        return stores

    def build_cookies(self, location_id: str, zip_code: str) -> dict | None:
        # returns None by default; walmart/kroger override
        return None

    # --- concrete public api ---

    def get_stores(self, zip_code: str, max_results: int = 10) -> list[dict[str, Any]]:
        # cache-aside read
        if cached := store_cache.get(self.retailer_name, zip_code):
            return cached[:max_results]

        stores = self._fetch_stores(zip_code, max_results)

        # cache-aside write
        if stores:
            store_cache.set(self.retailer_name, zip_code, stores)

        return stores

    def search_products(self, query: str, location_id: str | None = None, max_results: int = 5, **kwargs) -> list[dict[str, Any]]:
        # cache-aside read
        if location_id and (cached := product_cache.get(self.retailer_name, str(location_id), query)):
            return cached[:max_results]

        results = self._fetch_products(query, location_id=location_id, max_results=max_results, **kwargs)

        # cache-aside write
        if location_id and results:
            product_cache.set(self.retailer_name, str(location_id), query, results)

        return results
