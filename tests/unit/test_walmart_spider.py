import asyncio
import json
from unittest.mock import MagicMock

import orjson

from app.walmart.spider import WalmartSpider, run_walmart_batch


async def _collect_parse(spider, page):
    results = []
    async for item in spider.parse(page):
        results.append(item)
    return results


async def _collect_start_requests(spider):
    requests = []
    async for request in spider.start_requests():
        requests.append(request)
    return requests


def _next_data_html(items):
    next_data = {
        "props": {
            "pageProps": {
                "initialData": {
                    "searchResult": {
                        "itemStacks": [{"items": items}]
                    }
                }
            }
        }
    }
    return f'<script id="__NEXT_DATA__">{orjson.dumps(next_data).decode()}</script>'


def _walmart_item(product_id: str, store_id: str = "4673", **overrides):
    item = {
        "usItemId": product_id,
        "name": f"Product {product_id}",
        "brand": "Great Value",
        "salesUnit": "16 oz",
        "price": 3.49,
        "priceInfo": {
            "linePriceDisplay": "$3.49",
            "unitPrice": "$0.22/oz",
        },
        "rating": {
            "averageRating": 4.5,
            "numberOfReviews": 12,
        },
        "availabilityStatusV2": {
            "value": "IN_STOCK",
            "display": "In stock",
        },
        "image": {"url": f"https://example.com/{product_id}.jpg"},
        "canonicalUrl": f"/ip/product-{product_id}/{product_id}",
        "shortDescription": "A grocery product",
        "fulfillmentSummary": [{"storeId": store_id}],
        "__typename": "SearchProduct",
    }
    item.update(overrides)
    return item


class TestWalmartSpider:
    def test_start_requests_builds_encoded_urls(self):
        spider = WalmartSpider(["chicken breast"], "4673", "36830", max_results=10)

        requests = asyncio.run(_collect_start_requests(spider))

        assert len(requests) == 1
        assert requests[0].url == "https://www.walmart.com/search?q=chicken%20breast"
        assert requests[0].sid == "walmart"
        assert requests[0].meta == {"query": "chicken breast"}

    def test_location_cookies_are_converted_to_playwright_format(self):
        spider = WalmartSpider(["milk"], "4673", "36830", max_results=10)

        assert spider.cookie_dict["assortmentStoreId"] == "4673"
        assert {cookie["name"] for cookie in spider.cookies} == set(spider.cookie_dict)
        assert all(cookie["url"] == "https://www.walmart.com/" for cookie in spider.cookies)
        assert {
            "name": "assortmentStoreId",
            "value": "4673",
            "url": "https://www.walmart.com/",
        } in spider.cookies

    def test_configure_sessions_registers_async_stealthy_session(self, monkeypatch):
        captured = {}

        def fake_session(**kwargs):
            captured["session_kwargs"] = kwargs
            return "session"

        manager = MagicMock()
        monkeypatch.setattr("app.walmart.spider.AsyncStealthySession", fake_session)

        spider = WalmartSpider(["milk"], "4673", "36830", max_results=10)
        spider.configure_sessions(manager)

        assert captured["session_kwargs"] == {
            "max_pages": 1,
            "headless": True,
            "disable_resources": False,
            "network_idle": True,
            "solve_cloudflare": False,
            "real_chrome": False,
            "hide_canvas": True,
            "block_webrtc": True,
            "google_search": False,
            "timeout": 30000,
            "cookies": spider.cookies,
        }
        manager.add.assert_called_once_with("walmart", "session", default=True)

    def test_parse_returns_normalized_products(self, mock_page_factory):
        spider = WalmartSpider(["milk"], "4673", "36830", max_results=10)
        page = mock_page_factory(
            status=200,
            body=_next_data_html([_walmart_item("000111")]),
            url="https://www.walmart.com/search?q=milk",
        )
        page.meta = {"query": "milk"}

        results = asyncio.run(_collect_parse(spider, page))

        assert len(results) == 1
        product = results[0]
        assert product["retailer"] == "walmart"
        assert product["query"] == "milk"
        assert product["location_id"] == "4673"
        assert product["product_id"] == "000111"
        assert product["name"] == "Product 000111"
        assert product["price"] == 3.49
        assert product["price_display"] == "$3.49"
        assert product["image_url"] == "https://example.com/000111.jpg"
        assert product["availability"] == "In stock"
        assert product["url"] == "https://www.walmart.com/ip/product-000111/000111"

    def test_parse_respects_max_results(self, mock_page_factory):
        spider = WalmartSpider(["eggs"], "4673", "36830", max_results=3)
        items = [_walmart_item(str(index)) for index in range(10)]
        page = mock_page_factory(status=200, body=_next_data_html(items))
        page.meta = {"query": "eggs"}

        results = asyncio.run(_collect_parse(spider, page))

        assert len(results) == 3
        assert [item["product_id"] for item in results] == ["0", "1", "2"]

    def test_parse_skips_placeholders_and_items_without_name(self, mock_page_factory):
        spider = WalmartSpider(["bread"], "4673", "36830", max_results=10)
        items = [
            _walmart_item("valid"),
            _walmart_item("placeholder", name=None, __typename="SearchPlaceholderProduct"),
            _walmart_item("nameless", name=None),
        ]
        page = mock_page_factory(status=200, body=_next_data_html(items))
        page.meta = {"query": "bread"}

        results = asyncio.run(_collect_parse(spider, page))

        assert len(results) == 1
        assert results[0]["product_id"] == "valid"

    def test_parse_filters_products_unavailable_at_cookie_store(self, mock_page_factory):
        spider = WalmartSpider(["butter"], "4673", "36830", max_results=10)
        items = [
            _walmart_item("available", store_id="4673"),
            _walmart_item("unavailable", store_id="9999"),
        ]
        page = mock_page_factory(status=200, body=_next_data_html(items))
        page.meta = {"query": "butter"}

        results = asyncio.run(_collect_parse(spider, page))

        assert len(results) == 1
        assert results[0]["product_id"] == "available"

    def test_parse_skips_bad_items_and_continues(self, mock_page_factory):
        spider = WalmartSpider(["cheese"], "4673", "36830", max_results=10)
        items = [
            _walmart_item("bad", price={"amount": 3.49}),
            _walmart_item("good"),
        ]
        page = mock_page_factory(status=200, body=_next_data_html(items))
        page.meta = {"query": "cheese"}

        results = asyncio.run(_collect_parse(spider, page))

        assert len(results) == 1
        assert results[0]["product_id"] == "good"

    def test_parse_skips_non_200_without_crashing(self, mock_page_factory):
        spider = WalmartSpider(["bread"], "4673", "36830", max_results=10)
        page = mock_page_factory(status=503, body="Service unavailable")
        page.meta = {"query": "bread"}

        results = asyncio.run(_collect_parse(spider, page))

        assert results == []

    def test_is_blocked_detects_block_status(self, mock_page_factory):
        spider = WalmartSpider(["bread"], "4673", "36830", max_results=10)
        page = mock_page_factory(status=429, body="Too many requests")

        assert asyncio.run(spider.is_blocked(page)) is True

    def test_is_blocked_detects_soft_block_text(self, mock_page_factory):
        spider = WalmartSpider(["bread"], "4673", "36830", max_results=10)
        page = mock_page_factory(status=200, body="Pardon our interruption")

        assert asyncio.run(spider.is_blocked(page)) is True

    def test_is_blocked_detects_blocked_url(self, mock_page_factory):
        spider = WalmartSpider(["bread"], "4673", "36830", max_results=10)
        page = mock_page_factory(status=200, url="https://www.walmart.com/blocked")

        assert asyncio.run(spider.is_blocked(page)) is True


def test_run_walmart_batch_returns_spider_items(monkeypatch):
    items = [{"retailer": "walmart", "name": "Milk"}]
    spider = MagicMock()
    spider.start.return_value.items = items

    monkeypatch.setattr(
        "app.walmart.spider.WalmartSpider",
        lambda queries, location_id, zip_code, max_results: spider,
    )

    assert run_walmart_batch(["milk"], "4673", "36830", max_results=7) == items


def test_walmart_export_writes_jsonl(monkeypatch, tmp_path):
    from app.walmart import export

    output_path = tmp_path / "walmart_products.jsonl"
    items = [
        {"retailer": "walmart", "name": "Milk", "query": "milk"},
        {"retailer": "walmart", "name": "Eggs", "query": "eggs"},
    ]

    def fake_run_walmart_batch(queries, location_id, zip_code, max_results):
        assert len(queries) == 25
        assert location_id == "4673"
        assert zip_code == "36830"
        assert max_results == 7
        return items

    monkeypatch.setattr(export, "run_walmart_batch", fake_run_walmart_batch)

    export.main([
        "--location-id",
        "4673",
        "--zip-code",
        "36830",
        "--max-results",
        "7",
        "--output",
        str(output_path),
    ])

    lines = output_path.read_text(encoding="utf-8").splitlines()
    assert [json.loads(line) for line in lines] == items
