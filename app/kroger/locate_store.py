from app.utils import fetcher, store_selection
from app.kroger.constants import REFERER, STORE_LOCATOR_URL


class StoreNotFoundError(Exception):
    pass


def get_stores(zip_code, max_results=10):
    headers = {"Referer": f"{REFERER}stores/search"}
    params = {'filter.query': zip_code, 'projections': 'full'}

    page = fetcher.fetch(STORE_LOCATOR_URL, params=params, headers=headers)

    if page.status != 200:
        raise StoreNotFoundError(f"Status: {page.status} | URL: {page.url}")

    data = page.json()
    stores_data = data.get('data', {}).get('stores', [])

    results = []
    for store in stores_data[:max_results]:
        locale = store.get('locale', {})
        address = locale.get('address', {})
        location = locale.get('location', {})
        phone = store.get('phoneNumber', {})
        distance = store.get('distance', {})

        address_lines = address.get('addressLines', [])
        full_address = ', '.join(address_lines) if address_lines else ''
        city_state_zip = f"{address.get('cityTown', '')}, {address.get('stateProvince', '')} {address.get('postalCode', '')}"

        results.append({
            'name': store.get('vanityName'),
            'brand': store.get('brand'),
            'location_id': store.get('locationId'),
            'store_number': store.get('storeNumber'),
            'division': store.get('loyaltyDivisionNumber'),
            'address': full_address,
            'city_state_zip': city_state_zip,
            'phone': phone.get('pretty'),
            'distance': distance.get('pretty'),
            'is_open': store.get('isOpen'),
            'open_text': store.get('openText'),
            'hours': store.get('prettyHours', []),
            'lat': location.get('lat'),
            'lng': location.get('lng'),
            'departments': [d.get('vanityName') for d in store.get('departments', [])],
        })

    return results


def display_stores(stores, zip_code):
    print(f"\n{'='*60}")
    print(f"Found {len(stores)} Kroger stores near '{zip_code}'")
    print(f"{'='*60}\n")

    for i, store in enumerate(stores, start=1):
        status = "OPEN" if store['is_open'] else "CLOSED"
        print(f"{i}. {store['name']}")
        print(f"   {store['address']}")
        print(f"   {store['city_state_zip']}")
        print(f"   Phone: {store['phone']}")
        print(f"   Distance: {store['distance']} | {status} - {store['open_text']}")
        print(f"   Location ID: {store['location_id']}\n")


def find_and_select_store():
    zip_code = input("ZIP: ")
    stores = get_stores(zip_code)

    kroger_stores = [s for s in stores if s['brand'] == 'KROGER']

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
    kroger_stores = [s for s in stores if s['brand'] == 'KROGER']

    if not kroger_stores:
        print("No Kroger stores found.")
    else:
        display_stores(kroger_stores, zip_code)
        selected = store_selection.select_from_list(kroger_stores)
        if selected:
            print(f"\nSelected: {selected['name']}")
            print(f"Location ID: {selected['location_id']}")
