from app.walmart import locate_store, search_products
from app.utils import build_cookies


def main():
    query = input("Search Walmart for: ")

    use_store = input("Search for a specific store? (y/n): ").strip().lower()

    cookies = None
    if use_store == 'y':
        store_id, zip_code = locate_store.find_and_select_store()

        if not store_id:
            print("Store selection failed. Searching with default location.")
        else:
            cookies = build_cookies.build_location_cookies(store_id, zip_code)
            print(f"\nSearching store {store_id} (ZIP {zip_code}) for '{query}'...")

    results = search_products.search(query, cookies=cookies)
    search_products.display_results(results, query)


if __name__ == "__main__":
    main()
