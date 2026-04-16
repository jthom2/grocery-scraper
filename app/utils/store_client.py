from abc import ABC, abstractmethod
from typing import Any

from app.utils import store_selection, display
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

    def _filter_stores(self, stores: list[dict[str, Any]]) -> list[dict[str, Any]]:
        # identity by default; kroger overrides to filter by brand
        return stores

    def _build_cookies(self, location_id: str, zip_code: str) -> dict | None:
        # returns None by default; walmart/kroger override
        return None

    def _prompt_zip(self) -> str:
        return input("ZIP: ").strip()

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

    def find_and_select_store(self) -> tuple[str | None, str | None]:
        zip_code = self._prompt_zip()
        stores = self.get_stores(zip_code)

        if not stores:
            print(f"No {self.retailer_name.capitalize()} stores found.")
            return None, zip_code

        filtered = self._filter_stores(stores)
        if not filtered:
            print(f"No {self.retailer_name.capitalize()} stores found.")
            return None, zip_code

        display.display_stores(filtered, zip_code, self.retailer_name.capitalize())
        selected = store_selection.select_from_list(filtered)

        if not selected:
            return None, zip_code

        return selected['location_id'], zip_code

    def run_search_cli(self):
        query = input(f"Search {self.retailer_name.capitalize()} for: ")

        use_store = input("Search for a specific store? (y/n): ").strip().lower()

        location_id = None
        zip_code = None
        cookies = None
        if use_store == 'y':
            location_id, zip_code = self.find_and_select_store()

            if not location_id:
                print("Store selection failed. Searching with default location.")
            else:
                cookies = self._build_cookies(location_id, zip_code)
                print(f"\nSearching store {location_id} (ZIP {zip_code}) for '{query}'...")

        results = self.search_products(query, location_id=location_id, cookies=cookies, zip_code=zip_code)
        display.display_products(results, query, self.retailer_name.capitalize())
