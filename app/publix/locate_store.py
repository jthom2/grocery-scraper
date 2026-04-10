from app.publix.constants import REFERER, STORE_DIRECTORY_URL
from app.utils import fetcher, store_selection


def display_stores(stores, zip_code):
    print(f"\n{'='*60}")
    print(f"Found {len(stores)} Publix stores near '{zip_code}'")
    print(f"{'='*60}\n")

    for i, store in enumerate(stores, start=1):
        print(f"{i}. {store['name']}")
        print(f"   {store['address']}, {store['city']}, {store['state']} {store['zip']}")
        print(f"   Phone: {store['phone']}")
        print(f"   Location ID: {store['id']}\n")


def fetch_stores(zip_code, max_results=4):
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
        results.append({
            'id': _get('storeNumber'),
            'name': _get('name'),
            'short_name': _get('shortName'),
            'address': address.get('streetAddress'),
            'city': address.get('city'),
            'state': address.get('state'),
            'zip': address.get('zip'),
            'phone': _get('phoneNumbers', {}).get('Store')
        })

    return results


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

    return selected['id'], zip_code


if __name__ == "__main__":
    store_id, zip_code = find_and_select_store()
    print(f"Selected store {store_id} in ZIP {zip_code}")
