import logging
import urllib.parse

from scrapling.fetchers import AsyncStealthySession
from scrapling.spiders import Request, Response, Spider

from app.errors import ScraperBlockedError, ScraperParsingError
from app.kroger.client import (
    _dict_cookies_to_playwright,
    extract_initial_state,
    normalize_kroger_product,
)
from app.kroger.constants import REFERER, SEARCH_URL
from app.utils import build_kroger_cookies

logger = logging.getLogger(__name__)


class KrogerSpider(Spider):
    name = "kroger_batch_spider"
    allowed_domains = {"kroger.com", "www.kroger.com"}

    concurrent_requests = 1
    concurrent_requests_per_domain = 1
    download_delay = 12.0
    max_blocked_retries = 3

    def __init__(self, queries: list[str], location_id: str, max_results: int = 10, *args, **kwargs):
        self.queries = queries
        self.location_id = str(location_id)
        self.max_results = max_results
        self.cookie_dict = build_kroger_cookies.build_location_cookies(self.location_id)
        self.cookies = _dict_cookies_to_playwright(self.cookie_dict)
        self.headers = {"Referer": REFERER}
        super().__init__(*args, **kwargs)

    def configure_sessions(self, manager) -> None:
        manager.add(
            "kroger",
            AsyncStealthySession(
                max_pages=1,
                headless=True,
                disable_resources=False,
                network_idle=True,
                solve_cloudflare=True,
                real_chrome=True,
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
            params = {"query": query, "searchType": "default_search"}
            url = f"{SEARCH_URL}?{urllib.parse.urlencode(params, quote_via=urllib.parse.quote, safe='')}"
            yield Request(
                url,
                sid="kroger",
                extra_headers=self.headers,
                google_search=False,
                meta={"query": query},
            )

    async def is_blocked(self, response: Response) -> bool:
        if response.status in {403, 429}:
            return True

        response_url = str(response.url)
        response_text = getattr(response, "text", None) or getattr(response, "body", "") or ""
        if "/blocked" in response_url or "Access Denied" in response_text:
            return True

        return False

    async def parse(self, response: Response):
        query = response.meta.get("query")

        if response.status != 200:
            logger.error(f"Non-200 response ({response.status}) for query '{query}': {response.url}")
            return

        try:
            state = extract_initial_state(response)
            products_data = state["calypso"]["useCases"]["getProducts"]["search-grid"]["response"]["data"]["products"]
        except (KeyError, TypeError):
            logger.error(f"No Kroger products found in initial state for query '{query}'")
            return
        except (ScraperBlockedError, ScraperParsingError) as e:
            logger.error(f"Failed to parse Kroger initial state for query '{query}': {e}")
            return
        except Exception as e:
            logger.error(f"Unexpected Kroger parse failure for query '{query}': {e}")
            return

        for product_data in products_data[:self.max_results]:
            try:
                product = normalize_kroger_product(product_data, location_id=self.location_id)
            except Exception as e:
                logger.error(f"Failed to normalize Kroger product for query '{query}': {e}")
                continue

            product["query"] = query
            yield product

    async def on_error(self, request: Request, error: Exception) -> None:
        logger.error(f"Request failed in Kroger spider for {request.url}: {error}")


def run_kroger_batch(queries: list[str], location_id: str, max_results: int = 10):
    spider = KrogerSpider(queries, location_id, max_results)
    results = spider.start()
    return list(results.items)
