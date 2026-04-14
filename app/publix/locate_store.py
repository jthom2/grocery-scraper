from app.publix.constants import REFERER, STORE_DIRECTORY_URL
from app.models import normalize_location
from app.utils import fetcher, store_selection, display
from app.utils.store_cache import store_cache


# formats and prints store locations in a human-readable table layout
def display_stores(stores, zip_code):
    display.display_stores(stores, zip_code, "Publix")


# fetches and normalizes publix store locations from the store directory api
def fetch_stores(zip_code, max_results=4):
    # attempt to retrieve from cache (Cache-Aside: Read)
    if cached_stores := store_cache.get('publix', zip_code):
        return cached_stores[:max_results]

    request_count = max(1, int(max_results))
    params = {
        'types': 'R,G,H,N,S',
        'count': str(request_count),
        'distance': '50',
        'includeOpenAndCloseDates': 'true',
        'zip': zip_code,
        'isWebsite': 'true'
    }

    headers = {"Referer": REFERER}
    page = fetcher.fetch(STORE_DIRECTORY_URL, params=params, headers=headers)
    data = page.json()
    stores_data = data.get('stores', [])

    results = []
    for store in stores_data[:request_count]:
        _get = store.get
        address = _get('address', {})
        results.append(normalize_location({
            'retailer': 'publix',
            'location_id': str(_get('storeNumber')),
            'name': _get('name') or 'Publix',
            'address': address.get('streetAddress'),
            'city': address.get('city'),
            'state': address.get('state'),
            'postal_code': address.get('zip'),
            'phone': _get('phoneNumbers', {}).get('Store'),
            'metadata': {
                'short_name': _get('shortName'),
            },
        }))

    # store in cache for 24 hours (Cache-Aside: Write)
    if results:
        store_cache.set('publix', zip_code, results)

    return results


# prompts for zip code, fetches stores, and returns selected store location and zip code
def find_and_select_store():
    zip_code = input("Enter ZIP code: ").strip()
    stores = fetch_stores(zip_code)

    if not stores:
        print("No stores found.")
        return None, zip_code

    display_stores(stores, zip_code)
    selected = store_selection.select_from_list(stores)
    if not selected:
        return None, zip_code

    return selected['location_id'], zip_code


if __name__ == "__main__":
    store_id, zip_code = find_and_select_store()
    print(f"Selected store {store_id} in ZIP {zip_code}")
