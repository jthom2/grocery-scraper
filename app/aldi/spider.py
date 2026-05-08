import logging
import urllib.parse

import orjson
from scrapling.fetchers import AsyncStealthySession
from scrapling.spiders import Request, Response, Spider

from app.aldi.client import (
    build_items_url,
    build_search_context_from_page,
    build_search_placements_url,
    extract_item_ids,
)
from app.aldi.constants import REFERER, SEARCH_URL
from app.aldi.parser import normalize_item

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

    concurrent_requests = 3
    concurrent_requests_per_domain = 1
    download_delay = 2.0
    max_blocked_retries = 3

    def __init__(self, queries: list[str], zip_code: str, location_id: str | None = None, max_results: int = 10, *args, **kwargs):
        self.queries = queries
        self.zip_code = str(zip_code)
        self.location_id = str(location_id) if location_id else None
        self.max_results = max_results
        self.headers = {"Referer": REFERER}
        super().__init__(*args, **kwargs)

    def configure_sessions(self, manager) -> None:
        manager.add(
            "aldi",
            AsyncStealthySession(
                max_pages=1,
                headless=True,
                disable_resources=False,
                network_idle=False,
                solve_cloudflare=False,
                real_chrome=False,
                hide_canvas=True,
                block_webrtc=True,
                google_search=False,
                timeout=30000,
            ),
            default=True,
        )

    async def start_requests(self):
        for query in self.queries:
            params = {"k": query}
            url = f"{SEARCH_URL}?{urllib.parse.urlencode(params, quote_via=urllib.parse.quote, safe='')}"
            yield Request(
                url,
                sid="aldi",
                extra_headers=self.headers,
                google_search=False,
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
        # step 1: extract search context from the html page
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
        except Exception as e:
            logger.error(f"Failed to build search context for query '{query}': {e}")
            return

        # step 2: yield graphql request for search placements through the browser session
        placements_url = build_search_placements_url(
            query,
            search_context["zip_code"],
            search_context["location_id"],
            search_context["token"],
            max_results=self.max_results,
        )


        yield Request(
            placements_url,
            sid="aldi",
            extra_headers={"Referer": search_context["referer"]},
            google_search=False,
            callback=self.parse_placements,
            dont_filter=True,
            priority=10,
            meta={
                "query": query,
                "search_context": search_context,
            },
        )

    async def parse_placements(self, response: Response):
        # step 3: extract item ids from placements and yield item detail requests
        query = response.meta.get("query")
        search_context = response.meta.get("search_context")

        if response.status != 200:
            logger.error(f"Non-200 placements response ({response.status}) for query '{query}': {response.url}")
            return

        try:
            payload = orjson.loads(_response_text(response))
        except Exception:
            logger.error(f"Failed to parse placements JSON for query '{query}'")
            return

        data = payload.get("data") or {}
        placements = data.get("searchResultsPlacements", {}).get("placements", [])
        if not placements:
            logger.warning(f"No placements found for query '{query}'")
            return

        # fetch enough item ids to fill max_results after filtering
        item_ids = extract_item_ids(placements, max_ids=max(self.max_results * 2, 10))
        if not item_ids:
            logger.warning(f"No item IDs extracted for query '{query}'")
            return

        items_url = build_items_url(
            item_ids,
            search_context["location_id"],
            search_context["zip_code"],
        )

        yield Request(
            items_url,
            sid="aldi",
            extra_headers={"Referer": search_context["referer"]},
            google_search=False,
            callback=self.parse_items,
            dont_filter=True,
            priority=20,
            meta={
                "query": query,
                "location_id": search_context["location_id"],
            },
        )

    async def parse_items(self, response: Response):
        # step 4: normalize item data and yield products
        query = response.meta.get("query")
        location_id = response.meta.get("location_id")

        if response.status != 200:
            logger.error(f"Non-200 items response ({response.status}) for query '{query}': {response.url}")
            return

        try:
            payload = orjson.loads(_response_text(response))
        except Exception:
            logger.error(f"Failed to parse items JSON for query '{query}'")
            return

        data = payload.get("data") or {}
        items = data.get("items", [])
        if not items:
            return

        count = 0
        for item in items:
            if not item.get("name"):
                continue
            product = normalize_item(item, location_id)
            product["query"] = query
            yield product
            count += 1
            if count >= self.max_results:
                return

    async def on_error(self, request: Request, error: Exception) -> None:
        logger.error(f"Request failed in Aldi spider for {request.url}: {error}")


def run_aldi_batch(queries: list[str], zip_code: str, location_id: str | None = None, max_results: int = 10):
    spider = AldiSpider(queries, zip_code, location_id, max_results)
    results = spider.start()
    return list(results.items)
