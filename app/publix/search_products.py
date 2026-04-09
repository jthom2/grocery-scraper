import re
import urllib.parse

from scrapling import StealthyFetcher

from app.publix.constants import BASE_URL, SEARCH_URL


def search(query, store_id=None, max_results=15):

    url = f"{SEARCH_URL}?searchTerm={urllib.parse.quote(query)}"

    cookies = None
    if store_id:
        cookies = [{'name': 'Store', 'value': f'{{"storeNumber":"{store_id}"}}', 'url': f'{BASE_URL}/'}]

    fetcher = StealthyFetcher()
    page = fetcher.fetch(url, cookies=cookies, headless=True) # debug:  , network_idle=True

    # Verify store context if requested
    html = str(page.body)
    if store_id and f'"current_store": "{store_id}"' not in html:
        print("WARNING: Store context may not have persisted through redirects.")

    return extract_products(page, html, max_results)


def extract_products(page, html, max_results):
    
    products = []


    seen_ids = set()
    for match in re.finditer(r'href="/pd/([^/]+)/(RIO-PCI-\d+)[^"]*"[^>]*aria-label="([^"]+)"', html):
        if len(products) >= max_results:
            break

        name_slug = match.group(1)
        product_id = match.group(2)
        aria_label = match.group(3)

        if product_id in seen_ids:
            continue
                            ##############debug##########
        # price_match = re.match(r'(\$[\d.]+(?:\s+or\s+\d+\s+for\s+\$[\d.]+)?|\d+\s+for\s+\$[\d.]+)\s*-\s*(.+)', aria_label)


        price_match = re.match(r'(\$[\d.]+(?:\s+or\s+\d+\s+for\s+\$[\d.]+)?|\d+\s+for\s+\$[\d.]+(?:\s*/\s*[a-zA-Z\d\.]+)?|\$[\d.]+(?:\s*/\s*[a-zA-Z\d\.]+)?)\s*-\s*(.+)', aria_label)

        if not price_match:
            continue

        seen_ids.add(product_id)
        price = price_match.group(1)
        name = price_match.group(2).strip()
        brand = name.split()[0] if name else None

        products.append({
            'name': name,
            'brand': brand,
            'size': None,
            'price': price,
            'price_display': price,
            'unit_price': None,
            'promo_price': None,
            'image': None,
            'in_stock': True,
            'upc': product_id,
            'url': f"{BASE_URL}/pd/{name_slug}/{product_id}",
        })

    return products


def display_results(results, query):
    print(f"\n{'='*60}")
    print(f"Found {len(results)} products for '{query}'")
    print(f"{'='*60}\n")

    for i, product in enumerate(results, start=1):
        print(f"{i}. {product['name']}")
        if product['brand']:
            print(f"   Brand: {product['brand']}")
        price = product['price_display'] or product['price'] or 'N/A'
        print(f"   Price: {price}")
        if product['promo_price']:
            print(f"   Sale: {product['promo_price']}")
        if product['size']:
            print(f"   Size: {product['size']}")
        if product['url']:
            print(f"   URL: {product['url']}")
        print()


if __name__ == "__main__":
    query = input("Search Publix for: ")
    results = search(query)
    display_results(results, query)
