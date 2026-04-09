import sys
from pathlib import Path

project_root = str(Path(__file__).resolve().parent.parent.parent)
if project_root not in sys.path:
    sys.path.insert(0, project_root)
##################################################################
from app.kroger import locate_store, search_products
from app.utils import build_kroger_cookies


def main():
    query = input("Search Kroger for: ")

    use_store = input("Search for a specific store? (y/n): ").strip().lower()

    cookies = None
    if use_store == 'y':
        store_id, zip_code = locate_store.find_and_select_store()

        if not store_id:
            print("Store selection failed. Searching with default location.")
        else:
            cookies = build_kroger_cookies.build_location_cookies(store_id)
            print(f"\nSearching store {store_id} (ZIP {zip_code}) for '{query}'...")

    results = search_products.search(query, cookies)
    search_products.display_results(results, query)


if __name__ == "__main__":
    main()
