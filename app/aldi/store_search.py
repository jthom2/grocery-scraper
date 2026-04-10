from app.aldi import locate_store, search_products


def main():
    query = input("Search Aldi for: ")

    use_store = input("Search for a specific store? (y/n): ").strip().lower()

    shop_id = None
    zip_code = None
    if use_store == 'y':
        shop_id, zip_code = locate_store.find_and_select_store()

        if not shop_id:
            print("Store selection failed. Searching with default location.")
        else:
            print(f"\nSearching store {shop_id} (ZIP {zip_code}) for '{query}'...")

    results = search_products.search(query, shop_id=shop_id, zip_code=zip_code)
    search_products.display_results(results, query)


if __name__ == "__main__":
    main()
