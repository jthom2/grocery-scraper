import json
import re
import uuid

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
    variables = {
        'retailerSlug': RETAILER_SLUG,
        'postalCode': zip_code,
        'coordinates': {'latitude': latitude, 'longitude': longitude},
        'addressId': None,
        'allowCanonicalFallback': True,
    }
    extensions = {
        'persistedQuery': {
            'version': 1,
            'sha256Hash': SHOP_COLLECTION_SCOPED_HASH,
        }
    }
    params = {
        'operationName': 'ShopCollectionScoped',
        'variables': json.dumps(variables, separators=(',', ':')),
        'extensions': json.dumps(extensions, separators=(',', ':')),
    }

    page = fetcher.fetch(
        GRAPHQL_URL,
        params=params,
        cookies=cookies,
        headers={"Referer": referer},
    )

    if page.status != 200:
        return None

    data = page.json()
    if data.get('errors'):
        return None

    shops = (
        data.get('data', {})
        .get('shopCollection', {})
        .get('shops', [])
    )

    if not shops:
        return None

    return shops[0].get('retailerInventorySessionToken')


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
    variables = {
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
    }
    extensions = {
        'persistedQuery': {
            'version': 1,
            'sha256Hash': SEARCH_RESULTS_PLACEMENTS_HASH,
        }
    }
    params = {
        'operationName': 'SearchResultsPlacements',
        'variables': json.dumps(variables, separators=(',', ':')),
        'extensions': json.dumps(extensions, separators=(',', ':')),
    }

    page = fetcher.fetch(
        GRAPHQL_URL,
        params=params,
        cookies=cookies,
        headers={"Referer": referer},
    )

    if page.status != 200:
        return []

    data = page.json()
    if data.get('errors'):
        return []

    return (
        data.get('data', {})
        .get('searchResultsPlacements', {})
        .get('placements', [])
    )


def extract_item_ids(placements, max_ids=40):
    item_ids = []
    item_id_pattern = re.compile(r'^items_[0-9]+-[0-9]+$')

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

        if isinstance(value, str) and item_id_pattern.match(value) and value not in item_ids:
            item_ids.append(value)

    walk(placements)
    return item_ids


def fetch_items(item_ids, shop_id, zip_code, cookies, referer):
    variables = {
        'ids': item_ids,
        'shopId': str(shop_id),
        'zoneId': DEFAULT_ZONE_ID,
        'postalCode': zip_code,
    }
    extensions = {
        'persistedQuery': {
            'version': 1,
            'sha256Hash': ITEMS_HASH,
        }
    }
    params = {
        'operationName': 'Items',
        'variables': json.dumps(variables, separators=(',', ':')),
        'extensions': json.dumps(extensions, separators=(',', ':')),
    }

    page = fetcher.fetch(
        GRAPHQL_URL,
        params=params,
        cookies=cookies,
        headers={"Referer": referer},
    )

    if page.status != 200:
        return []

    data = page.json()
    if data.get('errors'):
        return []

    return data.get('data', {}).get('items', [])


def parse_price(price_display):
    if not price_display:
        return None

    match = re.search(r"\$([0-9]+(?:\.[0-9]+)?)", price_display)
    if not match:
        return None

    return float(match.group(1))


def normalize_item(item):
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

    return {
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
        'image': image,
        'in_stock': availability.get('available'),
        'stock_level': availability.get('stockLevel'),
        'availability': availability_view.get('stockLevelLabelString'),
        'upc': _get('legacyId') or _get('productId'),
        'url': f"{BASE_URL}/store/aldi/products/{evergreen_url}" if evergreen_url else None,
    }


def search(query, shop_id=None, zip_code=None, max_results=5):
    if max_results <= 0:
        return []

    search_page = fetcher.fetch(SEARCH_URL, params={'k': query})
    cookies = search_page.cookies
    referer = str(search_page.url)

    if not zip_code:
        zip_code = get_default_zip(cookies, referer)

    if not zip_code:
        return []

    latitude, longitude = get_coordinates(zip_code)
    if latitude is None or longitude is None:
        return []

    token = get_retailer_inventory_session_token(
        zip_code,
        latitude,
        longitude,
        cookies,
        referer,
    )
    if not token:
        return []

    if not shop_id:
        shop_id = get_default_shop_id(zip_code, cookies, referer)

    if not shop_id:
        return []

    placements = fetch_search_placements(
        query,
        zip_code,
        shop_id,
        token,
        cookies,
        referer,
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
        items = fetch_items(batch_ids, shop_id, zip_code, cookies, referer)
        if not items:
            continue

        for item in items:
            if not item.get('name'):
                continue

            results.append(normalize_item(item))
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
