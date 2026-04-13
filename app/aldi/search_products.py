import orjson
import re
import uuid
import time
from functools import lru_cache

from app.utils import fetcher, display
from app.utils.cache import TTLCache
from app.aldi.parser import normalize_item, parse_price
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


ITEM_ID_PATTERN = re.compile(r'"(items_[0-9]+-[0-9]+)"')

_SESSION_TOKEN_CACHE = TTLCache(ttl_seconds=15 * 60)


# executes a graphql persisted query and returns the data payload or empty dict on error
def run_persisted_query(operation_name, variables, query_hash, cookies, referer):
    params = {
        'operationName': operation_name,
        'variables': orjson.dumps(variables).decode(),
        'extensions': orjson.dumps({
            'persistedQuery': {
                'version': 1,
                'sha256Hash': query_hash,
            }
        }).decode(),
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


# looks up latitude and longitude for a given zip code using geolocation api
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


# retrieves the user's default zip code from aldi's location endpoint
def get_default_zip(cookies, referer):
    page = fetcher.fetch(
        IDP_LOCATION_URL,
        cookies=cookies,
        headers={"Referer": referer},
    )

    if page.status != 200:
        return None

    return page.json().get('postal_code')


# fetches and caches retailer inventory session token and shop id for search authorization
def get_retailer_inventory_session_token(zip_code, latitude, longitude, cookies, referer):
    cache_key = f"{zip_code}:{latitude}:{longitude}"
    cached = _SESSION_TOKEN_CACHE.get(cache_key)
    if cached:
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

    shops = data.get('shopCollection', {}).get('shops', [])
    if not shops:
        return None, None

    shop = shops[0]
    token = shop.get('retailerInventorySessionToken')
    shop_id = str(shop.get('id'))

    _SESSION_TOKEN_CACHE.set(cache_key, {'token': token, 'shop_id': shop_id})
    return token, shop_id


# queries the search api and retrieves product placement data for a given search term
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

    return data.get('searchResultsPlacements', {}).get('placements', [])


# extracts unique product item ids from search placements using regex pattern matching
def extract_item_ids(placements, max_ids=40):
    text = orjson.dumps(placements).decode()
    # Deduplicate while preserving order using a dictionary
    item_ids = list(dict.fromkeys(ITEM_ID_PATTERN.findall(text)))
    return item_ids[:max_ids]


# fetches detailed product information for a list of item ids
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


# establishes session, fetches credentials, and builds the complete search context needed for product queries
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


# processes a single item and adds it to results if valid
def _process_item(item, location_id, results, max_results):
    if not item.get('name'):
        return False
    results.append(normalize_item(item, location_id))
    return len(results) >= max_results


# processes batches of item ids and collects normalized products
def _process_items_batch(item_ids, search_context, max_results):
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
            if _process_item(item, search_context['location_id'], results, max_results):
                return results

    return results


# orchestrates the complete search flow from context setup through product normalization and filtering
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

    return _process_items_batch(item_ids, search_context, max_results)


# formats and prints search results in a human-readable table layout
def display_results(results, query):
    display.display_products(results, query, "Aldi")


if __name__ == "__main__":
    query = input("Search Aldi for: ")
    results = search(query)
    display_results(results, query)
