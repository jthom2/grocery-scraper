import logging
import random
import asyncio
from scrapling.spiders import Spider, Response, Request
from app.models import normalize_product
from app.utils import get_next_data
from app.walmart import build_cookies
from app.walmart.constants import SEARCH_URL, REFERER
from app.errors import ScraperBlockedError, ScraperNetworkError

logger = logging.getLogger(__name__)

class WalmartSpider(Spider):
    name = "walmart_batch_spider"
    
    # "Low and Slow" Configuration
    concurrent_requests = 1  # strictly one at a time
    download_delay = 12.0     # 12 seconds between requests
    max_blocked_retries = 3
    stealthy_headers = True
    impersonate = ["chrome", "firefox", "safari", "edge"] # cycle fingerprints

    def __init__(self, queries: list[str], location_id: str, zip_code: str, max_results: int = 10, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.queries = queries
        self.location_id = str(location_id)
        self.zip_code = str(zip_code)
        self.max_results = max_results
        
        self.cookies = build_cookies.build_location_cookies(self.location_id, self.zip_code)
        self.headers = {"Referer": REFERER}
        
    async def start_requests(self):
        for query in self.queries:
            url = f"{SEARCH_URL}?q={query}"
            yield Request(
                url, 
                cookies=self.cookies, 
                headers=self.headers,
                meta={"query": query},
                impersonate=random.choice(self.impersonate)
            )

    async def is_blocked(self, response: Response) -> bool:
        """Detect both hard and soft blocks."""
        if response.status in {403, 429}:
            return True
        if "/blocked" in response.url or "Pardon our interruption" in response.text:
            return True
        return False

    async def parse(self, response: Response):
        query = response.meta.get("query")
        
        if response.status != 200:
            logger.error(f"Non-200 response ({response.status}) for query '{query}': {response.url}")
            return

        try:
            next_data, data = get_next_data.get_next_data(response)
            item_stacks = data['props']['pageProps']['initialData']['searchResult']['itemStacks']
        except Exception as e:
            logger.error(f"Failed to parse next_data for query '{query}': {e}")
            return

        result_count = 0
        cookie_sid = self.cookies.get('assortmentStoreId')

        for stack in item_stacks:
            if result_count >= self.max_results:
                break
            for item in stack.get('items', ()):
                if result_count >= self.max_results:
                    break

                if not (name := item.get('name')) or item.get('__typename') == 'SearchPlaceholderProduct':
                    continue

                if cookie_sid:
                    fulfillment_opts = item.get('fulfillmentSummary') or []
                    is_in_store = any(str(f.get('storeId')) == str(cookie_sid) for f in fulfillment_opts)
                    if not is_in_store:
                        continue

                _get = item.get
                rating_data = _get('rating') or {}
                price_info = _get('priceInfo') or {}
                availability = _get('availabilityStatusV2') or {}
                image = _get('image')
                
                image_url = image.get('url') if isinstance(image, dict) else str(image) if image else None

                product = normalize_product({
                    'retailer': 'walmart',
                    'product_id': _get('usItemId'),
                    'location_id': self.location_id,
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
                    'url': f"https://www.walmart.com{_get('canonicalUrl', '')}",
                    'description': _get('shortDescription', ''),
                })
                
                product['query'] = query
                result_count += 1
                yield product

    async def handle_error(self, failure):
        logger.error(f"Request failed in spider: {failure}")


def run_walmart_batch(queries: list[str], location_id: str, zip_code: str, max_results: int = 10):
    spider = WalmartSpider(queries, location_id, zip_code, max_results)
    results = spider.start()
    return list(results.items)
