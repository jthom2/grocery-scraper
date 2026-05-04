from app.utils.store_client import BaseStoreClient
from app.utils import store_selection, display

def _find_and_select_store(client: BaseStoreClient) -> tuple[str | None, str | None]:
    zip_code = input("ZIP: ").strip()
    stores = client.get_stores(zip_code)

    if not stores:
        print(f"No {client.retailer_name.capitalize()} stores found.")
        return None, zip_code

    filtered = client.filter_stores(stores)
    if not filtered:
        print(f"No {client.retailer_name.capitalize()} stores found.")
        return None, zip_code

    display.display_stores(filtered, zip_code, client.retailer_name.capitalize())
    selected = store_selection.select_from_list(filtered)

    if not selected:
        return None, zip_code

    return selected['location_id'], zip_code

def run_interactive_search(client: BaseStoreClient) -> None:
    query = input(f"Search {client.retailer_name.capitalize()} for: ")

    use_store = input("Search for a specific store? (y/n): ").strip().lower()

    location_id = None
    zip_code = None
    cookies = None
    if use_store == 'y':
        location_id, zip_code = _find_and_select_store(client)

        if not location_id:
            print("Store selection failed. Searching with default location.")
        else:
            cookies = client.build_cookies(location_id, zip_code)
            print(f"\nSearching store {location_id} (ZIP {zip_code}) for '{query}'...")

    results = client.search_products(query, location_id=location_id, cookies=cookies, zip_code=zip_code)
    display.display_products(results, query, client.retailer_name.capitalize())
