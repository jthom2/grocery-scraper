import sys
from pathlib import Path

# Add project root to sys.path to allow imports from app
project_root = str(Path(__file__).resolve().parent.parent.parent)
if project_root not in sys.path:
    sys.path.insert(0, project_root)
##################################################################
from app.utils import get_next_data, fetcher

WALMART_REFERER = "https://www.walmart.com/"

# search Walmart for products by query.
# optionally pass location cookies to scope results to a specific store.
def search(query, cookies=None, max_results=5):
    url = 'https://www.walmart.com/search'
    headers = {"Referer": WALMART_REFERER}

    page = fetcher.fetch(url, params={'q': query}, cookies=cookies, headers=headers)

    # extract info hidden in __NEXT_DATA__ JSON
    next_data, data = get_next_data.get_next_data(page)

    # parse json data
    item_stacks = data['props']['pageProps']['initialData']['searchResult']['itemStacks']

    results = []
    result_count = 0

    for stack in item_stacks:
        if result_count >= max_results:
            break
        for item in stack.get('items', ()):
            if result_count >= max_results:
                break

            # skip invalid or placeholder items (e.g. ads)
            if not (name := item.get('name')) or item.get('__typename') == 'SearchPlaceholderProduct':
                continue

            # filter items not available in the selected store
            if cookies and (store_id := cookies.get('assortmentStoreId')):
                fulfillment_opts = item.get('fulfillmentSummary') or []
                is_in_store = any(str(f.get('storeId')) == str(store_id) for f in fulfillment_opts)
                if not is_in_store:
                    continue

            _get = item.get
            rating_data = _get('rating') or {}
            price_info = _get('priceInfo') or {}
            availability = _get('availabilityStatusV2') or {}

            results.append({
                'name': name,
                'brand': _get('brand'),
                'price': _get('price'),
                'price_display': price_info.get('linePriceDisplay'),
                'unit_price': price_info.get('unitPrice'),
                'was_price': price_info.get('wasPrice') or None,
                'savings': price_info.get('savings') or None,
                'rating': rating_data.get('averageRating'),
                'reviews': rating_data.get('numberOfReviews'),
                'image': _get('image'),
                'in_stock': availability.get('value') == 'IN_STOCK',
                'availability': availability.get('display'),
                'url': f"https://www.walmart.com{_get('canonicalUrl', '')}",
                'description': _get('shortDescription', ''),
            })
            result_count += 1

    return results


def display_results(results, query):
    print(f"\n{'='*60}")
    print(f"Found {len(results)} products for '{query}'")
    print(f"{'='*60}\n")

    for i, product in enumerate(results, start=1):
        print(f"{i}. {product['name']}")
        print(f"   Price: {product['price_display'] or product['price'] or 'N/A'}")
        print(f"   In Stock: {product['in_stock']}")
        print(f"   URL: {product['url']}\n")


# standalone entry point
if __name__ == "__main__":
    query = input("Search Walmart for: ")
    results = search(query)
    display_results(results, query)