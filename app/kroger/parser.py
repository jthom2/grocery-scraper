import re
import orjson
from app.models import normalize_product
from app.errors import ScraperBlockedError, ScraperParsingError
from app.kroger.constants import BASE_URL

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
def dict_cookies_to_playwright(cookie_dict, base_url=BASE_URL):
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
