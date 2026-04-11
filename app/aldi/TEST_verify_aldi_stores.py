"""
Aldi Store Data API Verification Script
Uses Scrapling library to fetch store data for a given zip code.
"""

import json
import sys
from scrapling.fetchers import FetcherSession

def get_aldi_stores(zip_code):

    api_url = f"https://www.aldi.us/idp/v1/shops?postal_code={zip_code}"
    warmup_url = "https://www.aldi.us/store/aldi/s"
    

    with FetcherSession(impersonate='chrome') as session:
        print(f"[*] Initializing session for zip code: {zip_code}...")
        

        #  __Host-instacart_sid required
        warmup_resp = session.get(warmup_url)
        if warmup_resp.status != 200:
            print(f"[!] Warmup failed with status: {warmup_resp.status}")
            return None

        print(f"[*] Fetching store data from internal API...")
        response = session.get(api_url)
        
        if response.status == 200:
            return response.json()
        else:
            print(f"[!] API request failed with status: {response.status}")
            print(f"    Response: {response.text[:200]}")
            return None

def display_stores(data, zip_code):

    if not data or 'shops' not in data:
        print(f"\n[!] No stores found for zip code {zip_code}.")
        return

    shops = data['shops']
    print(f"\n{'-'*60}")
    print(f"  ALDI Stores near '{zip_code}' (Found {len(shops)})")
    print(f"{'-'*60}\n")

    for i, shop in enumerate(shops, start=1):
        name = shop.get('location_name') or shop.get('name', 'ALDI')
        addr = shop.get('address', {})
        street = addr.get('street_address', 'N/A')
        city = addr.get('city', 'N/A')
        state = addr.get('state', 'N/A')
        postal = addr.get('postal_code', 'N/A')
        
        full_address = f"{street}, {city}, {state} {postal}"
        fulfillment = shop.get('fulfillment_option', 'N/A')
        loc_id = shop.get('id', 'N/A')
        loc_code = shop.get('location_code', 'N/A')

        print(f"{i:2}. {name}")
        print(f"    Address: {full_address}")
        print(f"    ID: {loc_id} | Code: {loc_code} | Service: {fulfillment}")
        print()

if __name__ == "__main__":
    target_zip = sys.argv[1] if len(sys.argv) > 1 else '30354'
    
    result = get_aldi_stores(target_zip)
    if result:
        display_stores(result, target_zip)
    else:
        print("\n[!] Failed to retrieve store data.")
