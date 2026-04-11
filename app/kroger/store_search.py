from app.kroger import locate_store, search_products
from app.utils import build_kroger_cookies


def main():
    query = input("Search Kroger for: ")

    use_store = input("Search for a specific store? (y/n): ").strip().lower()

    cookies = None
    location_id = None
    if use_store == 'y':
        location_id, zip_code = locate_store.find_and_select_store()

        if not location_id:
            print("Store selection failed. Searching with default location.")
        else:
            cookies = build_kroger_cookies.build_location_cookies(location_id)
            print(f"\nSearching store {location_id} (ZIP {zip_code}) for '{query}'...")

    results = search_products.search(query, cookies, location_id=location_id)
    search_products.display_results(results, query)


if __name__ == "__main__":
    main()
