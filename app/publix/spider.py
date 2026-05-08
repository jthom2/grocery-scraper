import logging
import urllib.parse

from scrapling.fetchers import AsyncStealthySession
from scrapling.spiders import Request, Response, Spider

from app.errors import ScraperParsingError
from app.publix.parser import extract_products
from app.publix.constants import BASE_URL, REFERER, SEARCH_URL

logger = logging.getLogger(__name__)


def _build_store_cookie(location_id: str | None) -> dict[str, str] | None:
    if not location_id:
        return None
    return {"Store": f'{{"storeNumber":"{location_id}"}}'}


def _dict_cookies_to_playwright(cookie_dict: dict[str, str] | None) -> list[dict[str, str]]:
    if not cookie_dict:
        return []
    return [
        {"name": name, "value": str(value), "url": f"{BASE_URL}/"}
        for name, value in cookie_dict.items()
    ]


def _response_html(response: Response) -> str:
    if text := getattr(response, "text", None):
        return text

    body = getattr(response, "body", "")
    if isinstance(body, bytes):
        return body.decode("utf-8", errors="replace")

    return str(body)


class PublixSpider(Spider):
    name = "publix_batch_spider"
    allowed_domains = {"publix.com", "www.publix.com"}

    concurrent_requests = 1
    concurrent_requests_per_domain = 1
    download_delay = 12.0
    max_blocked_retries = 3

    def __init__(self, queries: list[str], location_id: str | None = None, max_results: int = 10, *args, **kwargs):
        self.queries = queries
        self.location_id = str(location_id) if location_id else "1822"
        self.max_results = max_results
        self.cookie_dict = _build_store_cookie(self.location_id)
        self.cookies = _dict_cookies_to_playwright(self.cookie_dict)
        self.headers = {"Referer": REFERER}
        super().__init__(*args, **kwargs)

    def configure_sessions(self, manager) -> None:
        manager.add(
            "publix",
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
            params = {"searchTerm": query, "facet": "promoType::true"}
            url = f"{SEARCH_URL}?{urllib.parse.urlencode(params, quote_via=urllib.parse.quote, safe='')}"
            yield Request(
                url,
                sid="publix",
                extra_headers=self.headers,
                google_search=False,
                meta={"query": query},
            )

    async def is_blocked(self, response: Response) -> bool:
        if response.status in {403, 429}:
            return True

        response_url = str(response.url)
        response_text = _response_html(response).lower()
        if "/blocked" in response_url or "access denied" in response_text or "pardon our interruption" in response_text:
            return True

        return False

    async def parse(self, response: Response):
        query = response.meta.get("query")

        if response.status != 200:
            logger.error(f"Non-200 response ({response.status}) for query '{query}': {response.url}")
            return

        try:
            products = extract_products(response, _response_html(response), self.max_results, location_id=self.location_id)
        except ScraperParsingError as e:
            logger.error(f"Failed to parse Publix search result HTML for query '{query}': {e}")
            return
        except Exception as e:
            logger.error(f"Unexpected Publix parse failure for query '{query}': {e}")
            return

        for product in products:
            product["query"] = query
            yield product

    async def on_error(self, request: Request, error: Exception) -> None:
        logger.error(f"Request failed in Publix spider for {request.url}: {error}")


def run_publix_batch(queries: list[str], location_id: str | None = None, max_results: int = 10):
    spider = PublixSpider(queries, location_id, max_results)
    results = spider.start()
    return list(results.items)
