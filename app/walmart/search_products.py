from app.models import normalize_product
from app.utils import get_next_data, fetcher, display
from app.walmart.constants import REFERER, SEARCH_URL, BASE_URL


# fetches and normalizes walmart product search results with optional store filtering
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
            cookie_store_id = str(cookies.get('assortmentStoreId')) if cookies and cookies.get('assortmentStoreId') else None

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
                'location_id': str(location_id) if location_id else cookie_store_id,
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


# formats and prints search results in a human-readable table layout
def display_results(results, query):
    display.display_products(results, query, "Walmart")


if __name__ == "__main__":
    query = input("Search Walmart for: ")
    results = search(query)
    display_results(results, query)
