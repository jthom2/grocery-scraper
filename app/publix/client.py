import re
import urllib.parse
import logging

from scrapling import StealthyFetcher
from scrapling.fetchers import Fetcher
from lxml import html as lxml_html

from app.models import normalize_location, normalize_product
from app.utils import fetcher
from app.utils.store_client import BaseStoreClient
from app.publix.constants import BASE_URL, REFERER, SEARCH_URL, STORE_DIRECTORY_URL

from app.errors import ScraperBlockedError, ScraperParsingError, ScraperNetworkError

logger = logging.getLogger(__name__)


# checks if html contains product price data to validate search success
PRODUCT_CONTENT_PATTERN = re.compile(r'aria-label="\$[\d.]+')
REDIRECT_URL_PATTERN = re.compile(r'(searchtermredirect=[^&]+)')
HREF_PATTERN = re.compile(r'/pd/([^/]+)/(RIO-PCI-\d+)')
PRICE_PATTERN = re.compile(r'(\$[\d.]+(?:\s+or\s+\d+\s+for\s+\$[\d.]+)?|\d+\s+for\s+\$[\d.]+(?:\s*/\s*[a-zA-Z\d\.]+)?|\$[\d.]+(?:\s*/\s*[a-zA-Z\d\.]+)?)\s*-\s*(.+)')
NUMERIC_PRICE_PATTERN = re.compile(r'\$([0-9]+(?:\.[0-9]+)?)')


# checks if html contains product price data to validate search success
def _has_product_content(html):
    return bool(PRODUCT_CONTENT_PATTERN.search(html))


# extracts and normalizes product data from search result html using lxml dom traversal
# this approach is more resilient to HTML schema changes than regex pattern matching
def extract_products(page, html, max_results, location_id=None):
    products = []
    seen_ids = set()
    
    try:
        tree = lxml_html.fromstring(html)
    except (lxml_html.etree.ParserError, ValueError):
        raise ScraperParsingError(f"Failed to parse Publix search result HTML. Status: {page.status}", status_code=page.status, url=page.url)
    
    # find all product links using CSS selectors
    # target structure: <a href="/pd/{name_slug}/{product_id}" ... aria-label="{price} - {name}">
    product_links = tree.xpath('//a[contains(@href, "/pd/") and starts-with(@href, "/pd/") and contains(@aria-label, "$")]')
    
    for link in product_links:
        if len(products) >= max_results:
            break
        
        href = link.get('href', '')
        aria_label = link.get('aria-label', '')
        
        # extract product_id and name_slug from href using regex (resilient to href structure changes)
        href_match = HREF_PATTERN.search(href)
        if not href_match:
            continue
        
        name_slug = href_match.group(1)
        product_id = href_match.group(2)
        
        if product_id in seen_ids:
            continue
        
        # parse aria-label to extract price and product name
        price_match = PRICE_PATTERN.match(aria_label)
        
        if not price_match:
            continue
        
        seen_ids.add(product_id)
        price = price_match.group(1)
        name = price_match.group(2).strip()
        brand = name.split()[0] if name else None
        
        numeric_match = NUMERIC_PRICE_PATTERN.search(price)
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


class PublixClient(BaseStoreClient):

    @property
    def retailer_name(self) -> str:
        return "publix"

    def _prompt_zip(self) -> str:
        return input("Enter ZIP code: ").strip()

    def _fetch_stores(self, zip_code, max_results=4):
        request_count = max(1, int(max_results))
        params = {
            'types': 'R,G,H,N,S',
            'count': str(request_count),
            'distance': '50',
            'includeOpenAndCloseDates': 'true',
            'zip': zip_code,
            'isWebsite': 'true'
        }

        headers = {"Referer": REFERER}
        page = fetcher.fetch(STORE_DIRECTORY_URL, params=params, headers=headers)
        data = page.json()
        stores_data = data.get('stores', [])

        results = []
        for store in stores_data[:request_count]:
            _get = store.get
            address = _get('address', {})
            results.append(normalize_location({
                'retailer': 'publix',
                'location_id': str(_get('storeNumber')),
                'name': _get('name') or 'Publix',
                'address': address.get('streetAddress'),
                'city': address.get('city'),
                'state': address.get('state'),
                'postal_code': address.get('zip'),
                'phone': _get('phoneNumbers', {}).get('Store'),
                'metadata': {
                    'short_name': _get('shortName'),
                },
            }))

        return results

    # searches publix products with fast fetcher fallback to browser automation for complex scenarios
    def _fetch_products(self, query, location_id=None, max_results=15, **kwargs):
        url = f"{SEARCH_URL}?searchTerm={urllib.parse.quote(query, safe='')}&facet=promoType%3A%3Atrue"

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
            elif page.status == 403 or page.status == 429:
                logger.debug(f"Fetcher blocked ({page.status}), falling back to StealthyFetcher")
            else:
                logger.debug(f"Fetcher returned {page.status}, falling back to StealthyFetcher")

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
                redirect_url = REDIRECT_URL_PATTERN.sub(
                    r'\1&facet=promoType%3A%3Atrue',
                    redirect_url
                )
            elif "facet=" not in redirect_url:
                separator = "&" if "?" in redirect_url else "?"
                redirect_url = f"{redirect_url}{separator}facet=promoType%3A%3Atrue"

        sf = StealthyFetcher()
        page = sf.fetch(redirect_url, cookies=cookies, headless=True)

        if page.status == 403 or page.status == 429:
            raise ScraperBlockedError(f"Blocked by anti-bot: {page.status}", status_code=page.status, url=page.url)
        elif page.status != 200:
            raise ScraperNetworkError(f"Non-200 response: {page.status}", status_code=page.status, url=page.url)

        html = str(page.body)
        if location_id and f'"current_store": "{location_id}"' not in html:
            print("WARNING: Store context may not have persisted through redirects.")

        return extract_products(page, html, max_results, location_id)


def main():
    PublixClient().run_search_cli()


if __name__ == "__main__":
    main()
