import logging
import urllib.parse

from scrapling.fetchers import AsyncStealthySession
from scrapling.spiders import Spider, Response, Request

from app.utils import get_next_data
from app.walmart import build_cookies
from app.walmart.constants import BASE_URL, SEARCH_URL, REFERER
from app.walmart.parser import normalize_walmart_product

logger = logging.getLogger(__name__)


def _dict_cookies_to_playwright(cookie_dict: dict[str, str] | None) -> list[dict[str, str]]:
    if not cookie_dict:
        return []
    return [
        {"name": name, "value": str(value), "url": f"{BASE_URL}/"}
        for name, value in cookie_dict.items()
    ]


def _response_text(response: Response) -> str:
    if text := getattr(response, "text", None):
        return text

    body = getattr(response, "body", "")
    if isinstance(body, bytes):
        return body.decode("utf-8", errors="replace")

    return str(body)


class WalmartSpider(Spider):
    name = "walmart_batch_spider"
    allowed_domains = {"walmart.com", "www.walmart.com"}

    concurrent_requests = 3
    concurrent_requests_per_domain = 1
    download_delay = 2.0
    max_blocked_retries = 3

    def __init__(
        self,
        queries: list[str],
        location_id: str,
        zip_code: str,
        max_results: int = 10,
        *args,
        **kwargs,
    ):
        self.queries = queries
        self.location_id = str(location_id)
        self.zip_code = str(zip_code)
        self.max_results = max_results

        self.cookie_dict = build_cookies.build_location_cookies(self.location_id, self.zip_code)
        self.cookies = _dict_cookies_to_playwright(self.cookie_dict)
        self.headers = {"Referer": REFERER}
        super().__init__(*args, **kwargs)

    def configure_sessions(self, manager) -> None:
        manager.add(
            "walmart",
            AsyncStealthySession(
                max_pages=1,
                headless=True,
                disable_resources=False,
                network_idle=True,
                solve_cloudflare=False,
                real_chrome=False,
                hide_canvas=True,
                block_webrtc=True,
                google_search=False,
                timeout=30000,
                cookies=self.cookies,
            ),
            default=True,
        )

    async def start_requests(self):
        for query in self.queries:
            params = {"q": query}
            query_string = urllib.parse.urlencode(
                params,
                quote_via=urllib.parse.quote,
                safe='',
            )
            url = f"{SEARCH_URL}?{query_string}"
            yield Request(
                url,
                sid="walmart",
                extra_headers=self.headers,
                google_search=False,
                meta={"query": query},
            )

    async def is_blocked(self, response: Response) -> bool:
        if response.status in {403, 429}:
            return True

        response_url = str(response.url).lower()
        response_text = _response_text(response).lower()
        if (
            "/blocked" in response_url
            or "access denied" in response_text
            or "pardon our interruption" in response_text
        ):
            return True

        return False

    async def parse(self, response: Response):
        query = response.meta.get("query")

        if response.status != 200:
            logger.error(f"Non-200 response ({response.status}) for query '{query}': {response.url}")
            return

        try:
            _, data = get_next_data.get_next_data(response)
            item_stacks = (
                data['props']['pageProps']['initialData']['searchResult']['itemStacks']
                or []
            )
        except (KeyError, TypeError):
            logger.error(f"No Walmart products found in next_data for query '{query}'")
            return
        except Exception as e:
            logger.error(f"Failed to parse next_data for query '{query}': {e}")
            return

        result_count = 0
        cookie_sid = self.cookie_dict.get('assortmentStoreId')

        for stack in item_stacks:
            if result_count >= self.max_results:
                break
            for item in (stack or {}).get('items', ()):
                if result_count >= self.max_results:
                    break

                if not (name := item.get('name')) or item.get('__typename') == 'SearchPlaceholderProduct':
                    continue

                if cookie_sid:
                    fulfillment_opts = item.get('fulfillmentSummary') or []
                    is_in_store = any(str(f.get('storeId')) == str(cookie_sid) for f in fulfillment_opts)
                    if not is_in_store:
                        continue

                try:
                    product = normalize_walmart_product(item, self.location_id, cookie_sid)
                except Exception as e:
                    logger.error(f"Failed to normalize Walmart product for query '{query}': {e}")
                    continue

                product['query'] = query
                result_count += 1
                yield product

    async def on_error(self, request: Request, error: Exception) -> None:
        logger.error(f"Request failed in Walmart spider for {request.url}: {error}")


def run_walmart_batch(queries: list[str], location_id: str, zip_code: str, max_results: int = 10):
    spider = WalmartSpider(queries, location_id, zip_code, max_results)
    results = spider.start()
    return list(results.items)
