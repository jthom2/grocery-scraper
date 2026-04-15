from urllib.parse import quote

from app.models import normalize_location
from app.utils import zip2loc, get_next_data, fetcher, store_selection, display
from app.utils.store_cache import store_cache
from app.walmart.constants import STORE_DIRECTORY_URL


# converts zip code to city/state and fetches nearby walmart store locations
def find_stores(zip_code, max_stores=4):
    # attempt to retrieve from cache (Cache-Aside: Read)
    if cached_stores := store_cache.get('walmart', zip_code):
        return cached_stores[:max_stores]

    city, state = zip2loc.get_city_state(zip_code)

    if not city or not state:
        print(f"Error: Could not find location for zip code '{zip_code}'.")
        return []

    url = f'{STORE_DIRECTORY_URL}/{quote(state, safe="")}/{quote(city, safe="")}'
    page = fetcher.fetch(url)

    next_data, data = get_next_data.get_next_data(page)

    nearby_nodes = (
        data.get('props', {})
        .get('pageProps', {})
        .get('initialData', {})
        .get('initialDataNearbyNodes', {})
        .get('data', {})
        .get('nearByNodes', {})
        .get('nodes', [])
    )

    if not nearby_nodes:
        return []

    stores = []
    for node in nearby_nodes[:max_stores]:
        name = node.get('displayName') or node.get('name') or "Unknown Store"

        address_info = node.get('address', {})
        addr_line_1 = address_info.get('addressLineOne', '')
        addr_city = address_info.get('city', '')
        addr_state = address_info.get('state', '')
        addr_zip = address_info.get('postalCode', '')

        address_str = f"{addr_line_1}, {addr_city}, {addr_state} {addr_zip}".strip(", ")
        store_id = str(node.get('id', 'N/A'))

        stores.append(normalize_location({
            'retailer': 'walmart',
            'location_id': store_id,
            'name': name,
            'address': address_str or None,
            'city': addr_city or None,
            'state': addr_state or None,
            'postal_code': addr_zip or None,
            'metadata': {
                'address_info': address_info,
            },
        }))

    # store in cache for 24 hours (Cache-Aside: Write)
    if stores:
        store_cache.set('walmart', zip_code, stores)

    return stores


# formats and prints store locations in a human-readable table layout
def display_stores(stores, zip_code):
    display.display_stores(stores, zip_code, "Walmart")


# prompts for zip code, fetches stores, and returns selected store location and zip code
def find_and_select_store():
    zip_code = input("Enter zip code: ")
    stores = find_stores(zip_code)

    if not stores:
        print("No stores found.")
        return None, None

    display_stores(stores, zip_code)
    selected = store_selection.select_from_list(stores)

    if selected:
        print(f"\nSelected: {selected['name']} (ID: {selected['location_id']})")
        return selected['location_id'], zip_code

    return None, None


if __name__ == "__main__":
    store_id, zip_code = find_and_select_store()
    if store_id:
        print(f"\nStore ID: {store_id}, Zip: {zip_code}")
