import sys
from pathlib import Path

# Add project root to sys.path to allow imports from app
project_root = str(Path(__file__).resolve().parent.parent.parent)
if project_root not in sys.path:
    sys.path.insert(0, project_root)
##################################################################
from scrapling.fetchers import Fetcher
from app.utils import get_next_data
import orjson

query = input("Search Walmart for: ")

# scrape walmart search for a specific query
page = Fetcher.get(
    'https://www.walmart.com/search',
    params={'q': query},
    stealthy_headers=True,
    impersonate="chrome",
    timeout=10,
    retries=1,
)

# extract info hidden in __NEXT_DATA__ JSON
next_data, data = get_next_data.get_next_data(page)

item_stacks = data['props']['pageProps']['initialData']['searchResult']['itemStacks']

# prepare list of results
results = []
result_count = 0

for stack in item_stacks:
    if result_count >= 5:
        break
    for item in stack.get('items', ()):
        if result_count >= 5:
            break

        # skip over invalid or placeholder items (e.g. ads)
        if not (name := item.get('name')) or item.get('__typename') == 'SearchPlaceholderProduct':
            continue

        # speed up dict access
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

# console sanity check
print(f"\n{'='*60}")
print(f"Found {len(results)} products for '{query}'")
print(f"{'='*60}\n")