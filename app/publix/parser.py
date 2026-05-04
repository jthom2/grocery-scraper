import re
import logging
from lxml import html as lxml_html

from app.models import normalize_product
from app.publix.constants import BASE_URL
from app.errors import ScraperParsingError

logger = logging.getLogger(__name__)

# checks if html contains product price data to validate search success
PRODUCT_CONTENT_PATTERN = re.compile(r'aria-label="\$[\d.]+')
REDIRECT_URL_PATTERN = re.compile(r'(searchtermredirect=[^&]+)')
HREF_PATTERN = re.compile(r'/pd/([^/]+)/(RIO-PCI-\d+)')
PRICE_PATTERN = re.compile(r'(\$[\d.]+(?:\s+or\s+\d+\s+for\s+\$[\d.]+)?|\d+\s+for\s+\$[\d.]+(?:\s*/\s*[a-zA-Z\d\.]+)?|\$[\d.]+(?:\s*/\s*[a-zA-Z\d\.]+)?)\s*-\s*(.+)')
NUMERIC_PRICE_PATTERN = re.compile(r'\$([0-9]+(?:\.[0-9]+)?)')


# checks if html contains product price data to validate search success
def has_product_content(html):
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
