import logging
import urllib.parse

from scrapling import StealthyFetcher

from app.models import normalize_location, normalize_product
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

from app.errors import ScraperNetworkError, ScraperBlockedError, ScraperParsingError

logger = logging.getLogger(__name__)

_USE_BROWSER_POOL = False


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
    def _fetch_products(self, query, location_id=None, max_results=5, **kwargs):
        cookies = kwargs.get('cookies')
        params = {'query': query, 'searchType': 'default_search'}
        url = f"{SEARCH_URL}?{urllib.parse.urlencode(params, quote_via=urllib.parse.quote, safe='')}"

        playwright_cookies = _dict_cookies_to_playwright(cookies) if isinstance(cookies, dict) else cookies

        if _USE_BROWSER_POOL:
            pool = get_browser_pool()
            page = pool.fetch(url, cookies=playwright_cookies, google_search=False, extra_headers={'referer': REFERER})
            logger.debug(f"Kroger search using browser pool (request #{pool.request_count})")
        else:
            sf = StealthyFetcher()
            page = sf.fetch(url, cookies=playwright_cookies, headless=True, solve_cloudflare=False, google_search=False, extra_headers={'referer': REFERER})

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
