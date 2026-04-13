import json
import re
import uuid
import time
from functools import lru_cache

from app.models import normalize_product
from app.utils import fetcher
from app.aldi.constants import (
    BASE_URL,
    SEARCH_URL,
    GRAPHQL_URL,
    IDP_LOCATION_URL,
    IDP_SHOPS_URL,
    ZIP_LOOKUP_URL,
    RETAILER_SLUG,
    DEFAULT_ZONE_ID,
    SHOP_COLLECTION_SCOPED_HASH,
    SEARCH_RESULTS_PLACEMENTS_HASH,
    ITEMS_HASH,
)


ITEM_ID_PATTERN = re.compile(r'^items_[0-9]+-[0-9]+$')
PRICE_PATTERN = re.compile(r"\$([0-9]+(?:\.[0-9]+)?)")

_SESSION_TOKEN_CACHE_TTL_SECONDS = 15 * 60
_SESSION_TOKEN_CACHE = {}


def run_persisted_query(operation_name, variables, query_hash, cookies, referer):
    params = {
        'operationName': operation_name,
        'variables': json.dumps(variables, separators=(',', ':')),
        'extensions': json.dumps({
            'persistedQuery': {
                'version': 1,
                'sha256Hash': query_hash,
            }
        }, separators=(',', ':')),
    }

    page = fetcher.fetch(
        GRAPHQL_URL,
        params=params,
        cookies=cookies,
        headers={"Referer": referer},
    )
    if page.status != 200:
        return None

    payload = page.json()
    if payload.get('errors'):
        return None

    return payload.get('data') or {}


@lru_cache(maxsize=256)
def get_coordinates(zip_code):
    page = fetcher.fetch(f'{ZIP_LOOKUP_URL}/{zip_code}')

    if page.status != 200:
        return None, None

    places = page.json().get('places', [])
    if not places:
        return None, None

    lat_raw = places[0].get('latitude')
    lon_raw = places[0].get('longitude')

    try:
        return float(lat_raw), float(lon_raw)
    except (TypeError, ValueError):
        return None, None


def get_default_zip(cookies, referer):
    page = fetcher.fetch(
        IDP_LOCATION_URL,
        cookies=cookies,
        headers={"Referer": referer},
    )

    if page.status != 200:
        return None

    return page.json().get('postal_code')


def get_retailer_inventory_session_token(zip_code, latitude, longitude, cookies, referer):
    cache_key = f"{zip_code}:{latitude}:{longitude}"
    now = time.time()

    if cache_key in _SESSION_TOKEN_CACHE:
        cached = _SESSION_TOKEN_CACHE[cache_key]
        if cached['expires_at'] > now:
            return cached['token'], cached['shop_id']

    data = run_persisted_query(
        operation_name='ShopCollectionScoped',
        variables={
            'retailerSlug': RETAILER_SLUG,
            'postalCode': zip_code,
            'coordinates': {'latitude': latitude, 'longitude': longitude},
            'addressId': None,
            'allowCanonicalFallback': True,
        },
        query_hash=SHOP_COLLECTION_SCOPED_HASH,
        cookies=cookies,
        referer=referer,
    )
    if not data:
        return None, None

    shops = (
        data
        .get('shopCollection', {})
        .get('shops', [])
    )

    if not shops:
        return None, None

    shop = shops[0]
    token = shop.get('retailerInventorySessionToken')
    shop_id = str(shop.get('id'))

    _SESSION_TOKEN_CACHE[cache_key] = {
        'token': token,
        'shop_id': shop_id,
        'expires_at': now + _SESSION_TOKEN_CACHE_TTL_SECONDS,
    }

    return token, shop_id


def get_default_shop_id(zip_code, cookies, referer):
    page = fetcher.fetch(
        IDP_SHOPS_URL,
        params={'postal_code': zip_code},
        cookies=cookies,
        headers={"Referer": referer},
    )

    if page.status != 200:
        return None

    shops = page.json().get('shops', [])
    if not shops:
        return None

    return str(shops[0].get('id'))


def fetch_search_placements(query, zip_code, shop_id, token, cookies, referer, max_results=5):
    data = run_persisted_query(
        operation_name='SearchResultsPlacements',
        variables={
            'filters': [],
            'action': None,
            'query': query,
            'pageViewId': str(uuid.uuid4()),
            'retailerInventorySessionToken': token,
            'elevatedProductId': None,
            'searchSource': 'search',
            'disableReformulation': False,
            'disableLlm': False,
            'forceInspiration': False,
            'orderBy': 'bestMatch',
            'clusterId': None,
            'includeDebugInfo': False,
            'clusteringStrategy': None,
            'contentManagementSearchParams': {'itemGridColumnCount': 3},
            'shopId': str(shop_id),
            'postalCode': zip_code,
            'zoneId': DEFAULT_ZONE_ID,
            'first': max(max_results, 4),
        },
        query_hash=SEARCH_RESULTS_PLACEMENTS_HASH,
        cookies=cookies,
        referer=referer,
    )
    if not data:
        return []

    return (
        data
        .get('searchResultsPlacements', {})
        .get('placements', [])
    )


def extract_item_ids(placements, max_ids=40):
    item_ids = []
    seen_ids = set()

    def walk(value):
        if len(item_ids) >= max_ids:
            return

        if isinstance(value, dict):
            for nested in value.values():
                walk(nested)
            return

        if isinstance(value, list):
            for nested in value:
                walk(nested)
            return

        if isinstance(value, str) and ITEM_ID_PATTERN.match(value) and value not in seen_ids:
            item_ids.append(value)
            seen_ids.add(value)

    walk(placements)
    return item_ids


def fetch_items(item_ids, shop_id, zip_code, cookies, referer):
    data = run_persisted_query(
        operation_name='Items',
        variables={
            'ids': item_ids,
            'shopId': str(shop_id),
            'zoneId': DEFAULT_ZONE_ID,
            'postalCode': zip_code,
        },
        query_hash=ITEMS_HASH,
        cookies=cookies,
        referer=referer,
    )
    if not data:
        return []

    return data.get('items', [])


def parse_price(price_display):
    if not price_display:
        return None

    match = PRICE_PATTERN.search(price_display)
    if not match:
        return None

    return float(match.group(1))


def build_search_context(query, location_id=None, zip_code=None):
    search_page = fetcher.fetch(SEARCH_URL, params={'k': query})
    cookies = search_page.cookies
    referer = str(search_page.url)

    resolved_zip = zip_code or get_default_zip(cookies, referer)
    if not resolved_zip:
        return None

    latitude, longitude = get_coordinates(resolved_zip)
    if latitude is None or longitude is None:
        return None

    token, shop_id = get_retailer_inventory_session_token(
        resolved_zip,
        latitude,
        longitude,
        cookies,
        referer,
    )
    if not token:
        return None

    resolved_location_id = str(location_id) if location_id else shop_id
    if not resolved_location_id:
        return None

    return {
        'cookies': cookies,
        'referer': referer,
        'zip_code': resolved_zip,
        'location_id': resolved_location_id,
        'token': token,
    }


def normalize_item(item, location_id):
    _get = item.get

    price_view = (_get('price') or {}).get('viewSection', {})
    item_card = price_view.get('itemCard', {})
    item_details = price_view.get('itemDetails', {})
    availability = _get('availability') or {}
    availability_view = availability.get('viewSection', {})
    rating_data = _get('productRating') or {}
    view_section = _get('viewSection') or {}
    image = (view_section.get('itemImage') or {}).get('url')

    price_display = item_card.get('priceString') or item_details.get('priceString')
    unit_price = item_details.get('pricePerUnitString') or item_card.get('pricePerUnitString')
    was_price = item_card.get('fullPriceString') or item_details.get('fullPriceString')
    evergreen_url = _get('evergreenUrl')

    return normalize_product({
        'retailer': 'aldi',
        'location_id': str(location_id) if location_id else None,
        'product_id': _get('legacyId') or _get('productId'),
        'name': _get('name'),
        'brand': _get('brandName'),
        'size': _get('size'),
        'price': parse_price(price_display),
        'price_display': price_display,
        'unit_price': unit_price,
        'promo_price': None,
        'was_price': was_price,
        'rating': rating_data.get('averageStarRating') or rating_data.get('averageRating'),
        'reviews': rating_data.get('ratingCount') or rating_data.get('numberOfRatings'),
        'image_url': image,
        'in_stock': availability.get('available'),
        'stock_level': availability.get('stockLevel'),
        'availability': availability_view.get('stockLevelLabelString'),
        'url': f"{BASE_URL}/store/aldi/products/{evergreen_url}" if evergreen_url else None,
    })


def search(query, location_id=None, zip_code=None, max_results=5):
    if max_results <= 0:
        return []

    search_context = build_search_context(query, location_id=location_id, zip_code=zip_code)
    if not search_context:
        return []

    placements = fetch_search_placements(
        query,
        search_context['zip_code'],
        search_context['location_id'],
        search_context['token'],
        search_context['cookies'],
        search_context['referer'],
        max_results=max_results,
    )
    if not placements:
        return []

    item_ids = extract_item_ids(placements, max_ids=max(max_results * 8, 24))
    if not item_ids:
        return []

    results = []
    batch_size = max(max_results * 2, 8)
    for offset in range(0, len(item_ids), batch_size):
        batch_ids = item_ids[offset: offset + batch_size]
        items = fetch_items(
            batch_ids,
            search_context['location_id'],
            search_context['zip_code'],
            search_context['cookies'],
            search_context['referer'],
        )
        if not items:
            continue

        for item in items:
            if not item.get('name'):
                continue

            results.append(normalize_item(item, search_context['location_id']))
            if len(results) >= max_results:
                return results

    return results


def display_results(results, query):
    print(f"\n{'='*60}")
    print(f"Found {len(results)} products for '{query}'")
    print(f"{'='*60}\n")

    for i, product in enumerate(results, start=1):
        print(f"{i}. {product['name']}")
        if product['brand']:
            print(f"   Brand: {product['brand']}")
        if product['size']:
            print(f"   Size: {product['size']}")
        print(f"   Price: {product['price_display'] or product['price'] or 'N/A'}")
        if product['was_price']:
            print(f"   Was: {product['was_price']}")
        if product['unit_price']:
            print(f"   Unit: {product['unit_price']}")
        if product['rating']:
            print(f"   Rating: {product['rating']}/5 ({product['reviews']} reviews)")
        print(f"   In Stock: {product['in_stock']} ({product['stock_level']})")
        if product['url']:
            print(f"   URL: {product['url']}")
        print()


if __name__ == "__main__":
    query = input("Search Aldi for: ")
    results = search(query)
    display_results(results, query)
