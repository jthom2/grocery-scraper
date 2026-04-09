from app.publix.constants import REFERER, STORE_DIRECTORY_URL, BASE_URL
from app.utils import fetcher, store_selection
import json

zip_code = input("ZIP: ")

params = {'types': 'R,G,H,N,S',
          'count': '30',
          'distance': '50',
          'includeOpenAndCloseDates': 'true',
          'zip': zip_code,
          'isWebsite': 'true'  
        }

headers = {"Referer": REFERER}

page = fetcher.fetch(STORE_DIRECTORY_URL, params=params, headers=headers)

data = page.json()

stores_data = data.get('stores', {})

max_results=4
results = []
for store in stores_data[:max_results]:
    store_id = store.get('storeNumber', {})
    store_name = store.get('name', {})
    store_short_name = store.get('shortName', {})
    store_address = store.get('address', {}).get('streetAddress')
    store_city = store.get('address', {}).get('city')
    store_state = store.get('address', {}).get('state')
    store_zip = store.get('address', {}).get('zip')
    store_phone = store.get('phoneNumbers', {}).get('Store', {})



    results.append({
      'id': store_id,
      'name': store_name,
      'short_name': store_short_name,
      'address': store_address,
      'city': store_city,
      'state': store_state,
      'zip': store_zip,
      'phone': store_phone
    })

def display_stores(stores, zip_code):
    print(f"\n{'='*60}")
    print(f"Found {len(stores)} Publix stores near '{zip_code}'")
    print(f"{'='*60}\n")

    for i, store in enumerate(stores, start=1):
        print(f"{i}. {store['name']}")
        print(f"   {store['address']}, {store['city']}, {store['state']} {store['zip']}")
        print(f"   Phone: {store['phone']}")
        print(f"   Location ID: {store['id']}\n")

display_stores(stores=results, zip_code=zip_code)

selected = store_selection.select_from_list(results)
selected_id = selected['id']