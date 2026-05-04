import re
import orjson
import logging
import urllib.parse

from scrapling import StealthyFetcher

from app.models import normalize_location, normalize_product
from app.utils import fetcher
from app.utils.store_client import BaseStoreClient
from app.utils import build_kroger_cookies
from app.kroger.constants import SEARCH_URL, BASE_URL, REFERER, STORE_LOCATOR_URL
from app.kroger.browser_pool import get_browser_pool

from app.errors import ScraperNetworkError, ScraperBlockedError, ScraperParsingError

logger = logging.getLogger(__name__)

_USE_BROWSER_POOL = False


# extracts the initial state json object from page scripts
INITIAL_STATE_PATTERN = re.compile(r"JSON\.parse\('(.+)'\)", re.DOTALL)
NUMERIC_PRICE_PATTERN = re.compile(r'[\d.]+')


# extracts the initial state json object from page scripts
def extract_initial_state(page):
    if page.status == 403 or page.status == 429:
        raise ScraperBlockedError(f"Blocked by anti-bot: {page.status}", status_code=page.status, url=page.url)

    scripts = page.css('script')
    for script in scripts:
        text = script.text or ''
        if '__INITIAL_STATE__' in text:
            match = INITIAL_STATE_PATTERN.search(text)
            if match:
                json_str = match.group(1)
                json_str = json_str.encode('utf-8').decode('unicode_escape')
                return orjson.loads(json_str)
    raise ScraperParsingError(f"__INITIAL_STATE__ not found. Status: {page.status}", status_code=page.status, url=page.url)


# retrieves the front image url from product images list by size
def get_front_image(images, size='large'):
    for img in images or []:
        if img.get('perspective') == 'front' and img.get('size') == size:
            return img.get('url')
    return None


# extracts numeric price value from formatted price strings or numeric types
def extract_numeric_price(price_value):
    if price_value is None:
        return None
    if isinstance(price_value, (int, float)):
        return float(price_value)
    if isinstance(price_value, str):
        match = NUMERIC_PRICE_PATTERN.search(price_value)
        if match:
            return float(match.group(0))
    return None


# converts a flat cookie dict to playwright's list-of-dicts format
def _dict_cookies_to_playwright(cookie_dict, base_url=BASE_URL):
    if not cookie_dict:
        return []
    return [
        {'name': name, 'value': str(value), 'url': f'{base_url}/'}
        for name, value in cookie_dict.items()
    ]


def normalize_kroger_product(product, location_id=None):
    item = product.get('item') or {}
    price_data = product.get('price', {}).get('storePrices', {})
    regular = price_data.get('regular', {})
    promo = price_data.get('promo')
    inventory = product.get('inventory', {})
    ratings = item.get('ratingsAndReviewsAggregate', {})

    locations = inventory.get('locations', [])
    stock_level = locations[0].get('stockLevel') if locations else None

    return normalize_product({
        'retailer': 'kroger',
        'product_id': product.get('id'),
        'location_id': str(location_id) if location_id else None,
        'name': item.get('description'),
        'brand': (item.get('brand') or {}).get('name'),
        'size': item.get('customerFacingSize'),
        'price': extract_numeric_price(regular.get('price')),
        'price_display': regular.get('defaultDescription'),
        'unit_price': regular.get('equivalizedUnitPriceString'),
        'promo_price': promo.get('defaultDescription') if promo else None,
        'rating': ratings.get('averageRating'),
        'reviews': ratings.get('numberOfReviews'),
        'image_url': get_front_image(item.get('images')),
        'in_stock': stock_level in ('HIGH', 'LOW', 'MEDIUM') if stock_level else None,
        'stock_level': stock_level,
        'availability': stock_level,
        'url': f"{BASE_URL}/p/{item.get('seoDescription')}/{product.get('id')}",
    })


class KrogerClient(BaseStoreClient):

    @property
    def retailer_name(self) -> str:
        return "kroger"

    def _build_cookies(self, location_id, zip_code):
        return build_kroger_cookies.build_location_cookies(location_id)

    def _filter_stores(self, stores):
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
    KrogerClient().run_search_cli()


if __name__ == "__main__":
    main()
