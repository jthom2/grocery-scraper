from app.models import normalize_location
from app.utils import fetcher, store_selection, display
from app.kroger.constants import REFERER, STORE_LOCATOR_URL


class StoreNotFoundError(Exception):
    pass


# fetches and normalizes kroger store locations from the store locator api
def get_stores(zip_code, max_results=10):
    headers = {"Referer": f"{REFERER}stores/search"}
    params = {'filter.query': zip_code, 'projections': 'compact'}

    page = fetcher.fetch(STORE_LOCATOR_URL, params=params, headers=headers)

    if page.status != 200:
        raise StoreNotFoundError(f"Status: {page.status} | URL: {page.url}")

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


# formats and prints store locations in a human-readable table layout
def display_stores(stores, zip_code):
    display.display_stores(stores, zip_code, "Kroger")


# prompts for zip code, fetches stores, and returns selected store location and zip code
def find_and_select_store():
    zip_code = input("ZIP: ")
    stores = get_stores(zip_code)

    kroger_stores = [s for s in stores if s.get('metadata', {}).get('brand') == 'KROGER']

    if not kroger_stores:
        print("No Kroger stores found.")
        return None, None

    display_stores(kroger_stores, zip_code)
    selected = store_selection.select_from_list(kroger_stores)

    if selected:
        return selected['location_id'], zip_code

    return None, None


if __name__ == "__main__":
    zip_code = input("Enter zip code: ")
    stores = get_stores(zip_code)
    kroger_stores = [s for s in stores if s.get('metadata', {}).get('brand') == 'KROGER']

    if not kroger_stores:
        print("No Kroger stores found.")
    else:
        display_stores(kroger_stores, zip_code)
        selected = store_selection.select_from_list(kroger_stores)
        if selected:
            print(f"\nSelected: {selected['name']}")
            print(f"Location ID: {selected['location_id']}")
