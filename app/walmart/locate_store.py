import sys
from pathlib import Path

# Add project root to sys.path to allow imports from app
project_root = str(Path(__file__).resolve().parent.parent.parent)
if project_root not in sys.path:
    sys.path.insert(0, project_root)
##################################################################
from app.utils import zip2loc, get_next_data, fetcher

zip_input = input("Enter zip code: ")
city, state = zip2loc.get_city_state(zip_input)

if not city or not state:
    print(f"Error: Could not find location for zip code '{zip_input}'.")
    exit(1)



url = f'https://www.walmart.com/store-directory/{state}/{city}'

# scrape store locations based on city and state
page = fetcher.fetch(url)


# extract info hidden in __NEXT_DATA__ JSON
next_data, data = get_next_data.get_next_data(page)


# parses json data
nearby_nodes = data.get('props', {}).get('pageProps', {}).get('initialData', {}).get('initialDataNearbyNodes', {}).get('data', {}).get('nearByNodes', {}).get('nodes', [])

print(f"\n{'='*50}")
print(f"Walmart Stores in {city.title()}, {state.upper()}")
print(f"{'='*50}")














stores = []

# clean up data to easy to read format
if not nearby_nodes:
    print("No stores found.")
    exit(1)

for i, node in enumerate(nearby_nodes[:4], start=1):
    name = node.get('displayName') or node.get('name') or "Unknown Store"

    address_info = node.get('address', {})
    addr_line_1 = address_info.get('addressLineOne', '')
    addr_city = address_info.get('city', '')
    addr_state = address_info.get('state', '')
    addr_zip = address_info.get('postalCode', '')

    address_str = f"{addr_line_1}, {addr_city}, {addr_state} {addr_zip}".strip(", ")
    store_id = node.get('id', 'N/A')

    store_data = {
        'name': name,
        'store_id': store_id,
        'address': address_str,
        'address_info': address_info,
    }
    stores.append(store_data)

    print(f"{i}. {name}")
    print(f"   Store ID: {store_id}")
    print(f"   Address: {address_str}\n")

# store selection
selection = input("Select a store (1-4): ")
try:
    selection_idx = int(selection) - 1
    if 0 <= selection_idx < len(stores):
        selected_store = stores[selection_idx]
        print(f"\nSelected: {selected_store['name']} ID: {selected_store['store_id']}")
    else:
        print("Invalid selection.")
        exit(1)
except ValueError:
    print("Invalid input. Enter a number 1-4.")
    exit(1)


selected_id = selected_store['store_id']
