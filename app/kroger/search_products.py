import re
import orjson
import logging
import urllib.parse

from scrapling import StealthyFetcher

from app.models import normalize_product
from app.utils import display
from app.utils.product_cache import product_cache
from app.kroger.constants import SEARCH_URL, BASE_URL, REFERER
from app.kroger.browser_pool import get_browser_pool

logger = logging.getLogger(__name__)

_USE_BROWSER_POOL = False


from app.errors import ScraperParsingError, ScraperBlockedError


# extracts the initial state json object from page scripts
def extract_initial_state(page):
    if page.status == 403 or page.status == 429:
        raise ScraperBlockedError(f"Blocked by anti-bot: {page.status}", status_code=page.status, url=page.url)

    scripts = page.css('script')
    for script in scripts:
        text = script.text or ''
        if '__INITIAL_STATE__' in text:
            match = re.search(r"JSON\.parse\('(.+)'\)", text, re.DOTALL)
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
        match = re.search(r'[\d.]+', price_value)
        if match:
            return float(match.group(0))
    return None


# fetches and normalizes kroger product search results using browser automation
def search(query, cookies=None, location_id=None, max_results=5):
    # attempt to retrieve from cache (Cache-Aside: Read)
    if location_id and (cached_results := product_cache.get('kroger', str(location_id), query)):
        return cached_results[:max_results]

    params = {'query': query, 'searchType': 'default_search'}
    url = f"{SEARCH_URL}?{urllib.parse.urlencode(params)}"

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
        item = product.get('item') or {}
        price_data = product.get('price', {}).get('storePrices', {})
        regular = price_data.get('regular', {})
        promo = price_data.get('promo')
        inventory = product.get('inventory', {})
        ratings = item.get('ratingsAndReviewsAggregate', {})

        locations = inventory.get('locations', [])
        stock_level = locations[0].get('stockLevel') if locations else None

        results.append(normalize_product({
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
        }))

    # store in cache for 12 hours (Cache-Aside: Write)
    if location_id and results:
        product_cache.set('kroger', str(location_id), query, results)

    return results


# formats and prints search results in a human-readable table layout
def display_results(results, query):
    display.display_products(results, query, "Kroger")


if __name__ == "__main__":
    query = input("Search Kroger for: ")
    results = search(query)
    display_results(results, query)