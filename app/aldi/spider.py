import logging
import urllib.parse

from scrapling.spiders import Request, Response, Spider

from app.aldi.client import (
    _process_items_batch,
    build_search_context_from_page,
    extract_item_ids,
    fetch_search_placements,
)
from app.aldi.constants import REFERER, SEARCH_URL
from app.errors import ScraperBlockedError, ScraperNetworkError, ScraperParsingError

logger = logging.getLogger(__name__)


def _response_text(response: Response) -> str:
    if text := getattr(response, "text", None):
        return text

    body = getattr(response, "body", "")
    if isinstance(body, bytes):
        return body.decode("utf-8", errors="replace")

    return str(body)


class AldiSpider(Spider):
    name = "aldi_batch_spider"
    allowed_domains = {"aldi.us", "www.aldi.us"}

    concurrent_requests = 1
    concurrent_requests_per_domain = 1
    download_delay = 12.0
    max_blocked_retries = 3

    def __init__(self, queries: list[str], zip_code: str, location_id: str | None = None, max_results: int = 10, *args, **kwargs):
        self.queries = queries
        self.zip_code = str(zip_code)
        self.location_id = str(location_id) if location_id else None
        self.max_results = max_results
        self.headers = {"Referer": REFERER}
        super().__init__(*args, **kwargs)

    async def start_requests(self):
        for query in self.queries:
            params = {"k": query}
            url = f"{SEARCH_URL}?{urllib.parse.urlencode(params, quote_via=urllib.parse.quote, safe='')}"
            yield Request(
                url,
                headers=self.headers,
                meta={"query": query},
            )

    async def is_blocked(self, response: Response) -> bool:
        if response.status in {403, 429}:
            return True

        response_url = str(response.url)
        response_text = _response_text(response).lower()
        if "/blocked" in response_url or "access denied" in response_text or "pardon our interruption" in response_text:
            return True

        return False

    async def parse(self, response: Response):
        query = response.meta.get("query")

        if response.status != 200:
            logger.error(f"Non-200 response ({response.status}) for query '{query}': {response.url}")
            return

        try:
            search_context = build_search_context_from_page(
                response,
                location_id=self.location_id,
                zip_code=self.zip_code,
            )
            if not search_context:
                logger.error(f"Failed to build Aldi search context for query '{query}'")
                return

            placements = fetch_search_placements(
                query,
                search_context["zip_code"],
                search_context["location_id"],
                search_context["token"],
                search_context["cookies"],
                search_context["referer"],
                max_results=self.max_results,
            )
            if not placements:
                return

            item_ids = extract_item_ids(placements, max_ids=max(self.max_results * 8, 24))
            if not item_ids:
                return

            products = _process_items_batch(item_ids, search_context, self.max_results)
        except (ScraperBlockedError, ScraperNetworkError, ScraperParsingError) as e:
            logger.error(f"Failed to fetch Aldi products for query '{query}': {e}")
            return
        except Exception as e:
            logger.error(f"Unexpected Aldi parse failure for query '{query}': {e}")
            return

        for product in products:
            product["query"] = query
            yield product

    async def on_error(self, request: Request, error: Exception) -> None:
        logger.error(f"Request failed in Aldi spider for {request.url}: {error}")


def run_aldi_batch(queries: list[str], zip_code: str, location_id: str | None = None, max_results: int = 10):
    spider = AldiSpider(queries, zip_code, location_id, max_results)
    results = spider.start()
    return list(results.items)
