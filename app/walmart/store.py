import sys
from pathlib import Path

# Add project root to sys.path to allow imports from app
project_root = str(Path(__file__).resolve().parent.parent.parent)
if project_root not in sys.path:
    sys.path.insert(0, project_root)
##################################################################
from scrapling.fetchers import Fetcher
from app.utils import zip2loc
import orjson

zip_input = input("Enter zip code: ")
city, state = zip2loc.get_city_state(zip_input)

if not city or not state:
    print(f"Error: Could not find location for zip code '{zip_input}'.")
    exit(1)


# scrape function
page = Fetcher.get(
    f'https://www.walmart.com/store-directory/{state}/{city}',
    stealthy_headers=True,
    impersonate="chrome",
    timeout=10,
    retries=1,
)

# info is hidden in __NEXT_DATA__
next_data = page.css('script#__NEXT_DATA__')
if not next_data:
    print(f"Status: {page.status} | URL: {page.url}")
    exit(1)

# parses messy data
data = orjson.loads(str(next_data[0].text))
nearby_nodes = data.get('props', {}).get('pageProps', {}).get('initialData', {}).get('initialDataNearbyNodes', {}).get('data', {}).get('nearByNodes', {}).get('nodes', [])

print(f"\n{'='*50}")
print(f"Walmart Stores in {city.title()}, {state.upper()}")
print(f"{'='*50}")


total = 0


# clean up data to easy to read format
if not nearby_nodes:
    print("No stores found.")
else:
    for node in nearby_nodes:
        name = node.get('displayName') or node.get('name') or "Unknown Store"
        
        address_info = node.get('address', {})
        addr_line_1 = address_info.get('addressLineOne', '')
        addr_city = address_info.get('city', '')
        addr_state = address_info.get('state', '')
        addr_zip = address_info.get('postalCode', '')
        
        address_str = f"{addr_line_1}, {addr_city}, {addr_state} {addr_zip}".strip(", ")
        store_id = node.get('id', 'N/A')
        
        print(f"- {name}")
        print(f"  Store ID: {store_id}")
        print(f"  Address: {address_str}\n")
        total += 1
        if total > 5:
            break