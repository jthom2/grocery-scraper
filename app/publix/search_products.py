import re
import urllib.parse
import logging

from scrapling import StealthyFetcher
from scrapling.fetchers import Fetcher

from app.models import normalize_product
from app.publix.constants import BASE_URL, SEARCH_URL

logger = logging.getLogger(__name__)


# checks if html contains product price data to validate search success
def _has_product_content(html):
    return bool(re.search(r'aria-label="\$[\d.]+', html))


# searches publix products with fast fetcher fallback to browser automation for complex scenarios
def search(query, location_id=None, max_results=15):

    url = f"{SEARCH_URL}?searchTerm={urllib.parse.quote(query)}&facet=promoType%3A%3Atrue"

    cookie_dict = None
    cookies = None
    if location_id:
        cookie_dict = {'Store': f'{{"storeNumber":"{location_id}"}}'}
        cookies = [{'name': 'Store', 'value': f'{{"storeNumber":"{location_id}"}}', 'url': f'{BASE_URL}/'}]

    # Strategy 1: Try standard Fetcher first (fast path ~500-800ms)
    try:
        page = Fetcher.get(url, cookies=cookie_dict, follow_redirects=True)

        if page.status == 200:
            html = str(page.body)
            store_context_ok = not location_id or f'"current_store": "{location_id}"' in html

            if store_context_ok and _has_product_content(html):
                logger.debug("Publix search succeeded with standard Fetcher (fast path)")
                return extract_products(page, html, max_results, location_id)

            logger.debug("Fetcher returned 200 but content validation failed, falling back to StealthyFetcher")

    except Exception as e:
        logger.debug(f"Fetcher failed: {e}, falling back to StealthyFetcher")

    # Strategy 2: Fallback to StealthyFetcher (slow path ~2000-2500ms)
    # Handles 403 errors, bot detection, and complex redirect scenarios
    initial = Fetcher.get(url, cookies=cookie_dict, follow_redirects=False)
    redirect_url = url

    if initial.status in (301, 302, 303, 307, 308):
        redirect_url = initial.headers.get('location', '')
        if redirect_url and not redirect_url.startswith('http'):
            redirect_url = f"{BASE_URL}{redirect_url}"

        if "searchtermredirect=" in redirect_url and "facet=" not in redirect_url:
            redirect_url = re.sub(
                r'(searchtermredirect=[^&]+)',
                r'\1&facet=promoType%3A%3Atrue',
                redirect_url
            )
        elif "facet=" not in redirect_url:
            separator = "&" if "?" in redirect_url else "?"
            redirect_url = f"{redirect_url}{separator}facet=promoType%3A%3Atrue"

    fetcher = StealthyFetcher()
    page = fetcher.fetch(redirect_url, cookies=cookies, headless=True)

    html = str(page.body)
    if location_id and f'"current_store": "{location_id}"' not in html:
        print("WARNING: Store context may not have persisted through redirects.")

    return extract_products(page, html, max_results, location_id)


# extracts and normalizes product data from search result html using regex pattern matching
def extract_products(page, html, max_results, location_id=None):
    
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

        price_match = re.match(r'(\$[\d.]+(?:\s+or\s+\d+\s+for\s+\$[\d.]+)?|\d+\s+for\s+\$[\d.]+(?:\s*/\s*[a-zA-Z\d\.]+)?|\$[\d.]+(?:\s*/\s*[a-zA-Z\d\.]+)?)\s*-\s*(.+)', aria_label)

        if not price_match:
            continue

        seen_ids.add(product_id)
        price = price_match.group(1)
        name = price_match.group(2).strip()
        brand = name.split()[0] if name else None
        numeric_match = re.search(r'\$([0-9]+(?:\.[0-9]+)?)', price)
        parsed_price = None
        if numeric_match:
            try:
                parsed_price = float(numeric_match.group(1))
            except ValueError:
                logger.warning("Failed to parse numeric Publix price from '%s'", price)
                parsed_price = None

        products.append(normalize_product({
            'retailer': 'publix',
            'product_id': product_id,
            'location_id': str(location_id) if location_id else None,
            'name': name,
            'brand': brand,
            'size': None,
            'price': parsed_price,
            'price_display': price,
            'unit_price': None,
            'promo_price': None,
            'image_url': None,
            'in_stock': True,
            'url': f"{BASE_URL}/pd/{name_slug}/{product_id}",
            'metadata': {'raw_price_text': price},
        }))

    return products


# formats and prints search results in a human-readable table layout
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
