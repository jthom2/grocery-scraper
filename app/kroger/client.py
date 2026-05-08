import logging
import random
import threading
import time
import urllib.parse

from scrapling import StealthyFetcher

from app.models import normalize_location
from app.utils import fetcher
from app.utils.store_client import BaseStoreClient
from app.kroger import build_cookies as build_kroger_cookies
from app.kroger.constants import SEARCH_URL, BASE_URL, REFERER, STORE_LOCATOR_URL
from app.kroger.browser_pool import get_browser_pool
from app.kroger.parser import (
    dict_cookies_to_playwright as _dict_cookies_to_playwright,
    extract_initial_state,
    normalize_kroger_product,
)

from app.errors import ScraperNetworkError, ScraperBlockedError

logger = logging.getLogger(__name__)

_USE_BROWSER_POOL = False
_POOL_MIN_INTERVAL_SECONDS = 1.25
_POOL_JITTER_SECONDS = 0.35
_POOL_MAX_ATTEMPTS = 2
_POOL_BACKOFF_SECONDS = 1.5
_POOL_WARMUP_DONE = False
_POOL_RATE_LOCK = threading.Lock()
_POOL_WARMUP_LOCK = threading.Lock()
_POOL_LAST_REQUEST_AT = 0.0


class KrogerClient(BaseStoreClient):

    @property
    def retailer_name(self) -> str:
        return "kroger"

    def build_cookies(self, location_id, zip_code):
        return build_kroger_cookies.build_location_cookies(location_id)

    def filter_stores(self, stores):
        # isolate kroger-branded stores from the parent company's multi-brand response
        return [s for s in stores if s.get('metadata', {}).get('brand') == 'KROGER']

    # fetches and normalizes kroger store locations from the store locator api
    def _fetch_stores(self, zip_code, max_results=10):
        headers = {"Referer": f"{REFERER}stores/search"}
        params = {'filter.query': zip_code, 'projections': 'compact'}

        page = fetcher.fetch(STORE_LOCATOR_URL, params=params, headers=headers)

        if page.status == 403 or page.status == 429:
            raise ScraperBlockedError(f"Blocked by anti-bot: {page.status}", status_code=page.status, url=page.url)
        elif page.status != 200:
            raise ScraperNetworkError(f"Non-200 response: {page.status}", status_code=page.status, url=page.url)

        data = page.json()
        stores_data = data.get('data', {}).get('stores', [])

        results = []
        for store in stores_data[:max_results]:
            brand = (store.get('brand') or store.get('banner') or '').upper()
            locale = store.get('locale', {})
            address = locale.get('address', {})
            location = locale.get('location', {})
            phone = store.get('phoneNumber', {})
            distance = store.get('distance', {})

            address_lines = address.get('addressLines', [])
            full_address = ', '.join(address_lines) if address_lines else ''
            city_state_zip = f"{address.get('cityTown', '')}, {address.get('stateProvince', '')} {address.get('postalCode', '')}"

            results.append(normalize_location({
                'retailer': 'kroger',
                'name': store.get('vanityName') or 'Kroger',
                'location_id': str(store.get('locationId')),
                'address': full_address or None,
                'city': address.get('cityTown'),
                'state': address.get('stateProvince'),
                'postal_code': address.get('postalCode'),
                'phone': phone.get('pretty'),
                'distance': distance.get('pretty'),
                'is_open': store.get('isOpen'),
                'open_text': store.get('openText'),
                'latitude': location.get('lat'),
                'longitude': location.get('lng'),
                'metadata': {
                    'brand': brand,
                    'store_number': store.get('storeNumber'),
                    'division': store.get('loyaltyDivisionNumber'),
                    'hours': store.get('prettyHours', []),
                    'departments': [d.get('vanityName') for d in store.get('departments', [])],
                    'city_state_zip': city_state_zip,
                },
            }))

        return results

    # fetches and normalizes kroger product search results using browser automation
    def _fetch_page_primary(self, url, cookies):
        sf = StealthyFetcher()
        return sf.fetch(
            url,
            cookies=cookies,
            headless=True,
            real_chrome=True,
            solve_cloudflare=False,
            google_search=False,
            extra_headers={'referer': REFERER},
        )

    # extracts non-sensitive block markers from response headers
    def _extract_block_telemetry(self, response, fetch_mode):
        headers = (response.headers or {}) if hasattr(response, 'headers') else {}
        normalized_headers = {str(k).lower(): str(v) for k, v in headers.items()}
        set_cookie = normalized_headers.get('set-cookie', '').lower()
        response_url = str(getattr(response, "url", ""))
        path = urllib.parse.urlparse(response_url).path if response_url else ""

        return {
            "fetch_mode": fetch_mode,
            "status": getattr(response, "status", None),
            "path": path,
            "server": normalized_headers.get('server'),
            "akamai_grn": normalized_headers.get('akamai-grn'),
            "has_abck_cookie": '_abck=' in set_cookie,
            "has_bm_cookie": 'bm_' in set_cookie,
        }

    # logs block diagnostics for actionable runtime troubleshooting
    def _log_blocked_response(self, response, fetch_mode):
        logger.warning("Kroger blocked response: %s", self._extract_block_telemetry(response, fetch_mode))

    # keeps blocked responses explicit across all fetch paths
    def _raise_if_blocked(self, response, fetch_mode):
        status = getattr(response, "status", None)
        if status in {403, 429}:
            self._log_blocked_response(response, fetch_mode)
            raise ScraperBlockedError(
                f"Blocked by anti-bot: {status}",
                status_code=status,
                url=getattr(response, "url", None),
            )

    # avoids high-frequency pool calls that can trigger stricter bot defenses
    def _pace_pool_request(self):
        global _POOL_LAST_REQUEST_AT
        with _POOL_RATE_LOCK:
            now = time.monotonic()
            elapsed = now - _POOL_LAST_REQUEST_AT
            delay = _POOL_MIN_INTERVAL_SECONDS - elapsed
            if delay > 0:
                time.sleep(delay + random.uniform(0.0, _POOL_JITTER_SECONDS))
            _POOL_LAST_REQUEST_AT = time.monotonic()

    # performs a one-time browser warmup request before search calls
    def _warmup_pool(self, pool):
        global _POOL_WARMUP_DONE
        if _POOL_WARMUP_DONE:
            return
        with _POOL_WARMUP_LOCK:
            if _POOL_WARMUP_DONE:
                return
            try:
                self._pace_pool_request()
                warmup_page = pool.fetch(
                    BASE_URL,
                    cookies=None,
                    google_search=False,
                    extra_headers={'referer': REFERER},
                )
                if getattr(warmup_page, "status", None) in {403, 429}:
                    self._log_blocked_response(warmup_page, "browser_pool_warmup")
            except Exception as e:
                logger.debug(f"Kroger browser pool warmup failed: {e}")
            finally:
                _POOL_WARMUP_DONE = True

    # retries blocked/failed requests using pooled real-browser session
    def _fetch_page_pool(self, url, cookies):
        pool = get_browser_pool()
        self._warmup_pool(pool)

        last_error = None
        for attempt in range(1, _POOL_MAX_ATTEMPTS + 1):
            try:
                self._pace_pool_request()
                page = pool.fetch(
                    url,
                    cookies=cookies,
                    google_search=False,
                    extra_headers={'referer': REFERER},
                )
                logger.debug(f"Kroger search using browser pool (request #{pool.request_count}, attempt {attempt})")
                self._raise_if_blocked(page, "browser_pool")
                return page
            except ScraperBlockedError as e:
                last_error = e
                if attempt >= _POOL_MAX_ATTEMPTS:
                    raise
                time.sleep(_POOL_BACKOFF_SECONDS + random.uniform(0.0, _POOL_JITTER_SECONDS))
            except Exception as e:
                last_error = e
                if attempt >= _POOL_MAX_ATTEMPTS:
                    raise ScraperNetworkError(
                        f"Kroger browser pool fetch failed: {e}",
                        url=url,
                    ) from e
                time.sleep(_POOL_BACKOFF_SECONDS + random.uniform(0.0, _POOL_JITTER_SECONDS))

        if last_error:
            raise last_error
        raise ScraperNetworkError("Kroger browser pool fetch failed", url=url)

    def _fetch_products(self, query, location_id=None, max_results=5, **kwargs):
        cookies = kwargs.get('cookies')
        params = {'query': query, 'searchType': 'default_search'}
        url = f"{SEARCH_URL}?{urllib.parse.urlencode(params, quote_via=urllib.parse.quote, safe='')}"

        playwright_cookies = _dict_cookies_to_playwright(cookies) if isinstance(cookies, dict) else cookies

        if _USE_BROWSER_POOL:
            page = self._fetch_page_pool(url, playwright_cookies)
        else:
            try:
                page = self._fetch_page_primary(url, playwright_cookies)
                self._raise_if_blocked(page, "stealthy_fetcher")
            except ScraperBlockedError as e:
                logger.debug(f"Kroger primary fetch blocked, retrying via browser pool: {e}")
                page = self._fetch_page_pool(url, playwright_cookies)
            except Exception as e:
                logger.debug(f"Kroger primary fetch failed, retrying via browser pool: {e}")
                page = self._fetch_page_pool(url, playwright_cookies)

        state = extract_initial_state(page)

        try:
            products_data = state['calypso']['useCases']['getProducts']['search-grid']['response']['data']['products']
        except (KeyError, TypeError):
            return []

        results = []
        for product in products_data[:max_results]:
            results.append(normalize_kroger_product(product, location_id=location_id))

        return results


def main():
    from app.cli import run_interactive_search
    run_interactive_search(KrogerClient())


if __name__ == "__main__":
    main()
