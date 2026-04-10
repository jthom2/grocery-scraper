from app.publix import locate_store, search_products


def main():
    query = input("Search Publix for: ")

    use_store = input("Search for a specific store? (y/n): ").strip().lower()

    store_id = None
    if use_store == 'y':
        store_id, zip_code = locate_store.find_and_select_store()

        if not store_id:
            print("Store selection failed. Searching with default location.")
        else:
            print(f"\nSearching store {store_id} (ZIP {zip_code}) for '{query}'...")

    results = search_products.search(query, store_id=store_id)
    search_products.display_results(results, query)


if __name__ == "__main__":
    main()
