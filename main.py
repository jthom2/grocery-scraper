import json
from scrapling.fetchers import StealthyFetcher


query = input("Search Walmart for: ")

# Crawl function
page = StealthyFetcher.fetch(
    f'https://www.walmart.com/search?q={query}',
    headless=True,
    disable_resources=True
)

# Extract product data from the embedded __NEXT_DATA__ JSON
next_data = page.css('script#__NEXT_DATA__')
if not next_data:
    print(f"Status: {page.status} | URL: {page.url}")
    exit(1)

data = json.loads(next_data[0].text)
item_stacks = data['props']['pageProps']['initialData']['searchResult']['itemStacks']

# Adds products & their info to array
results = []
for stack in item_stacks:
    for item in stack.get('items', []):
        if len(results) >= 10:
            break
            
        # Skips ads
        if not item.get('name') or item.get('__typename') == 'SearchPlaceholderProduct':
            continue

        rating_data = item.get('rating', {}) or {}
        price_info = item.get('priceInfo', {}) or {}
        availability = item.get('availabilityStatusV2', {}) or {}

        results.append({
            'name': item.get('name'),
            'brand': item.get('brand'),
            'price': item.get('price'),
            'price_display': price_info.get('linePriceDisplay'),
            'unit_price': price_info.get('unitPrice'),
            'was_price': price_info.get('wasPrice') or None,
            'savings': price_info.get('savings') or None,
            'rating': rating_data.get('averageRating'),
            'reviews': rating_data.get('numberOfReviews'),
            'image': item.get('image'),
            'in_stock': availability.get('value') == 'IN_STOCK',
            'availability': availability.get('display'),
            'url': f"https://www.walmart.com{item.get('canonicalUrl', '')}",
            'description': item.get('shortDescription', ''),
        })
    if len(results) >= 10:
        break

# Print how many results found
print(f"\n{'='*60}")
print(f"Found {len(results)} products for '{query}'")
print(f"{'='*60}\n")

##### Prints results
# for i, product in enumerate(results, 1):
#     print(f"{i}. {product['name']}")
#     if product['brand']:
#         print(f"   Brand: {product['brand']}")
#     print(f"   Price: {product['price_display'] or 'N/A'}", end="")
#     if product['unit_price']:
#         print(f" ({product['unit_price']})", end="")
#     if product['was_price']:
#         print(f"  [was {product['was_price']}]", end="")
#     if product['savings']:
#         print(f"  SAVE {product['savings']}", end="")
#     print()
#     if product['rating']:
#         stars = '★' * int(product['rating']) + '☆' * (5 - int(product['rating']))
#         print(f"   Rating: {stars} {product['rating']}/5 ({product['reviews']:,} reviews)")
#     print(f"   Stock: {'✅ ' + product['availability'] if product['in_stock'] else '❌ Out of Stock'}")
#     print(f"   URL: {product['url']}")
#     print()