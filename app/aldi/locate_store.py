from app.models import normalize_location
from app.utils import fetcher, store_selection
from app.aldi.constants import STORE_FRONT_URL, IDP_SHOPS_URL


def get_stores(zip_code, max_results=10):
    entry = fetcher.fetch(STORE_FRONT_URL)
    cookies = entry.cookies
    headers = {"Referer": STORE_FRONT_URL}

    page = fetcher.fetch(
        IDP_SHOPS_URL,
        params={'postal_code': zip_code},
        cookies=cookies,
        headers=headers,
    )

    if page.status != 200:
        return []

    shops_data = page.json().get('shops', [])
    stores = []

    for shop in shops_data[:max_results]:
        _get = shop.get
        address = _get('address', {})
        _get_address = address.get

        street = _get_address('street_address', '')
        city = _get_address('city', '')
        state = _get_address('state', '')
        postal = _get_address('postal_code', '')

        address_line = f"{street}, {city}, {state} {postal}".strip(", ")
        city_state_zip = f"{city}, {state} {postal}".strip(", ")

        stores.append(normalize_location({
            'retailer': 'aldi',
            'name': _get('location_name') or _get('name') or 'ALDI',
            'location_id': str(_get('id')),
            'address': address_line or None,
            'city': city or None,
            'state': state or None,
            'postal_code': postal or None,
            'phone': _get('phone_number'),
            'service_type': _get('fulfillment_option'),
            'metadata': {
                'location_code': _get('location_code'),
                'city_state_zip': city_state_zip,
            },
        }))

    return stores


def display_stores(stores, zip_code):
    print(f"\n{'='*60}")
    print(f"Found {len(stores)} Aldi stores near '{zip_code}'")
    print(f"{'='*60}\n")

    for i, store in enumerate(stores, start=1):
        print(f"{i}. {store['name']}")
        print(f"   {store['address']}")
        if store['phone']:
            print(f"   Phone: {store['phone']}")
        print(f"   Service: {store['service_type']}")
        location_code = store.get('metadata', {}).get('location_code')
        print(f"   Shop ID: {store['location_id']} | Location Code: {location_code}\n")


def find_and_select_store():
    zip_code = input("ZIP: ").strip()
    stores = get_stores(zip_code)

    if not stores:
        print("No Aldi stores found.")
        return None, None

    display_stores(stores, zip_code)
    selected = store_selection.select_from_list(stores)

    if selected:
        return selected['location_id'], zip_code

    return None, None


if __name__ == "__main__":
    zip_code = input("ZIP: ").strip()
    stores = get_stores(zip_code)

    if not stores:
        print("No Aldi stores found.")
    else:
        display_stores(stores, zip_code)
        selected = store_selection.select_from_list(stores)
        if selected:
            print(f"\nSelected: {selected['name']}")
            print(f"Shop ID: {selected['location_id']}")
