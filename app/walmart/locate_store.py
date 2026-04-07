import sys
from pathlib import Path

# Add project root to sys.path to allow imports from app
project_root = str(Path(__file__).resolve().parent.parent.parent)
if project_root not in sys.path:
    sys.path.insert(0, project_root)
##################################################################
from urllib.parse import quote

from app.utils import zip2loc, get_next_data, fetcher

# Look up nearby Walmart stores for a zip code.
def find_stores(zip_code, max_stores=4):
    city, state = zip2loc.get_city_state(zip_code)

    if not city or not state:
        print(f"Error: Could not find location for zip code '{zip_code}'.")
        return []

    url = f'https://www.walmart.com/store-directory/{quote(state)}/{quote(city)}'
    page = fetcher.fetch(url)

    # extract info hidden in __NEXT_DATA__ JSON
    next_data, data = get_next_data.get_next_data(page)

    # parses json data
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
        store_id = node.get('id', 'N/A')

        stores.append({
            'name': name,
            'store_id': store_id,
            'address': address_str,
            'address_info': address_info,
        })

    return stores


def display_and_select(stores, zip_code):
    print(f"\n{'='*50}")
    print(f"Walmart Stores near {zip_code}")
    print(f"{'='*50}")

    for i, store in enumerate(stores, start=1):
        print(f"{i}. {store['name']}")
        print(f"   Store ID: {store['store_id']}")
        print(f"   Address: {store['address']}\n")

    selection = input(f"Select a store (1-{len(stores)}): ")
    try:
        idx = int(selection) - 1
        if 0 <= idx < len(stores):
            selected = stores[idx]
            print(f"\nSelected: {selected['name']} (ID: {selected['store_id']})")
            return selected['store_id'], zip_code
        else:
            print("Invalid selection.")
            return None, None
    except ValueError:
        print(f"Invalid input. Enter a number 1-{len(stores)}.")
        return None, None

# ask for zip → find stores → select one.
def find_and_select_store():
    zip_code = input("Enter zip code: ")
    stores = find_stores(zip_code)

    if not stores:
        print("No stores found.")
        return None, None

    return display_and_select(stores, zip_code)


# standalone entry point
if __name__ == "__main__":
    store_id, zip_code = find_and_select_store()
    if store_id:
        print(f"\nStore ID: {store_id}, Zip: {zip_code}")
