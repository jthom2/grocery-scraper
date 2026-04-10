from app.models import normalize_product
from app.utils import get_next_data, fetcher
from app.walmart.constants import REFERER, SEARCH_URL, BASE_URL


def search(query, cookies=None, location_id=None, max_results=5):
    headers = {"Referer": REFERER}

    page = fetcher.fetch(SEARCH_URL, params={'q': query}, cookies=cookies, headers=headers)

    next_data, data = get_next_data.get_next_data(page)

    item_stacks = data['props']['pageProps']['initialData']['searchResult']['itemStacks']

    results = []
    result_count = 0

    for stack in item_stacks:
        if result_count >= max_results:
            break
        for item in stack.get('items', ()):
            if result_count >= max_results:
                break

            if not (name := item.get('name')) or item.get('__typename') == 'SearchPlaceholderProduct':
                continue

            if cookies and (store_id := cookies.get('assortmentStoreId')):
                fulfillment_opts = item.get('fulfillmentSummary') or []
                is_in_store = any(str(f.get('storeId')) == str(store_id) for f in fulfillment_opts)
                if not is_in_store:
                    continue

            _get = item.get
            rating_data = _get('rating') or {}
            price_info = _get('priceInfo') or {}
            availability = _get('availabilityStatusV2') or {}
            image = _get('image')
            if isinstance(image, dict):
                image_url = image.get('url')
            else:
                image_url = str(image) if image else None

            results.append(normalize_product({
                'retailer': 'walmart',
                'product_id': _get('usItemId'),
                'location_id': str(location_id) if location_id else (str(store_id) if cookies and (store_id := cookies.get('assortmentStoreId')) else None),
                'name': name,
                'brand': _get('brand'),
                'size': _get('salesUnit'),
                'price': _get('price'),
                'price_display': price_info.get('linePriceDisplay'),
                'unit_price': price_info.get('unitPrice'),
                'was_price': price_info.get('wasPrice') or None,
                'rating': rating_data.get('averageRating'),
                'reviews': rating_data.get('numberOfReviews'),
                'image_url': image_url,
                'in_stock': availability.get('value') == 'IN_STOCK',
                'availability': availability.get('display'),
                'url': f"{BASE_URL}{_get('canonicalUrl', '')}",
                'description': _get('shortDescription', ''),
            }))
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


if __name__ == "__main__":
    query = input("Search Walmart for: ")
    results = search(query)
    display_results(results, query)
