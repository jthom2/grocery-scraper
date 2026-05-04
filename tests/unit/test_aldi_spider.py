import asyncio
import json
from unittest.mock import MagicMock

import pytest

from app.aldi.parser import normalize_item
from app.aldi.spider import AldiSpider, run_aldi_batch


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


def _aldi_item(product_id: str):
    return {
        "name": f"Product {product_id}",
        "legacyId": product_id,
        "brandName": "Aldi",
        "size": "12 oz",
        "price": {
            "viewSection": {
                "itemCard": {
                    "priceString": "$3.49",
                    "pricePerUnitString": "$0.29/oz",
                }
            }
        },
        "availability": {
            "available": True,
            "stockLevel": "HIGH",
            "viewSection": {"stockLevelLabelString": "In Stock"},
        },
        "evergreenUrl": f"product-{product_id}",
    }


class TestAldiSpider:
    def test_start_requests_builds_encoded_urls(self):
        spider = AldiSpider(["chicken breast"], "30303", location_id="12345", max_results=10)

        requests = asyncio.run(_collect_start_requests(spider))

        assert len(requests) == 1
        assert requests[0].url == "https://www.aldi.us/store/aldi/s?k=chicken%20breast"
        assert requests[0].meta == {"query": "chicken breast"}

    def test_parse_returns_normalized_products(self, mock_page_factory, monkeypatch):
        spider = AldiSpider(["milk"], "30303", location_id="12345", max_results=10)
        page = mock_page_factory(
            status=200,
            cookies={"session": "abc"},
            url="https://www.aldi.us/store/aldi/s?k=milk",
        )
        page.meta = {"query": "milk"}

        monkeypatch.setattr(
            "app.aldi.spider.build_search_context_from_page",
            lambda response, location_id, zip_code: {
                "cookies": response.cookies,
                "referer": str(response.url),
                "zip_code": zip_code,
                "location_id": location_id,
                "token": "token-123",
            },
        )
        monkeypatch.setattr(
            "app.aldi.spider.fetch_search_placements",
            lambda *args, **kwargs: [{"item": {"id": "items_100-1"}}],
        )
        monkeypatch.setattr("app.aldi.spider.extract_item_ids", lambda placements, max_ids: ["items_100-1"])
        monkeypatch.setattr(
            "app.aldi.spider._process_items_batch",
            lambda item_ids, search_context, max_results: [
                normalize_item(_aldi_item("item1"), search_context["location_id"])
            ],
        )

        results = asyncio.run(_collect_parse(spider, page))

        assert len(results) == 1
        product = results[0]
        assert product["retailer"] == "aldi"
        assert product["query"] == "milk"
        assert product["location_id"] == "12345"
        assert product["product_id"] == "item1"
        assert product["name"] == "Product item1"
        assert product["price"] == 3.49
        assert product["price_display"] == "$3.49"

    def test_parse_respects_max_results(self, mock_page_factory, monkeypatch):
        spider = AldiSpider(["eggs"], "30303", location_id="12345", max_results=2)
        page = mock_page_factory(status=200, cookies={"session": "abc"}, url="https://www.aldi.us/store/aldi/s?k=eggs")
        page.meta = {"query": "eggs"}

        monkeypatch.setattr(
            "app.aldi.spider.build_search_context_from_page",
            lambda response, location_id, zip_code: {
                "cookies": response.cookies,
                "referer": str(response.url),
                "zip_code": zip_code,
                "location_id": location_id,
                "token": "token-123",
            },
        )
        monkeypatch.setattr("app.aldi.spider.fetch_search_placements", lambda *args, **kwargs: [{"items": ["items_100-1"]}])
        monkeypatch.setattr("app.aldi.spider.extract_item_ids", lambda placements, max_ids: ["items_100-1", "items_100-2"])

        def fake_process_items_batch(item_ids, search_context, max_results):
            return [
                normalize_item(_aldi_item(f"item{i}"), search_context["location_id"])
                for i in range(1, max_results + 1)
            ]

        monkeypatch.setattr("app.aldi.spider._process_items_batch", fake_process_items_batch)

        results = asyncio.run(_collect_parse(spider, page))

        assert len(results) == 2
        assert [item["product_id"] for item in results] == ["item1", "item2"]

    def test_parse_skips_non_200_without_crashing(self, mock_page_factory):
        spider = AldiSpider(["bread"], "30303", location_id="12345", max_results=10)
        page = mock_page_factory(status=503, body="Service unavailable")
        page.meta = {"query": "bread"}

        results = asyncio.run(_collect_parse(spider, page))

        assert results == []

    def test_is_blocked_detects_block_status(self, mock_page_factory):
        spider = AldiSpider(["bread"], "30303", location_id="12345", max_results=10)
        page = mock_page_factory(status=429, body="Too many requests")

        assert asyncio.run(spider.is_blocked(page)) is True


def test_run_aldi_batch_returns_spider_items(monkeypatch):
    items = [{"retailer": "aldi", "name": "Milk"}]
    spider = MagicMock()
    spider.start.return_value.items = items

    monkeypatch.setattr("app.aldi.spider.AldiSpider", lambda queries, zip_code, location_id, max_results: spider)

    assert run_aldi_batch(["milk"], "30303", location_id="12345", max_results=7) == items


def test_aldi_export_writes_jsonl(monkeypatch, tmp_path):
    from app.aldi import export

    output_path = tmp_path / "aldi_products.jsonl"
    items = [
        {"retailer": "aldi", "name": "Milk", "query": "milk"},
        {"retailer": "aldi", "name": "Eggs", "query": "eggs"},
    ]

    def fake_run_aldi_batch(queries, zip_code, location_id, max_results):
        assert len(queries) == 25
        assert zip_code == "30303"
        assert location_id == "12345"
        assert max_results == 7
        return items

    monkeypatch.setattr(export, "run_aldi_batch", fake_run_aldi_batch)

    export.main([
        "--zip-code",
        "30303",
        "--location-id",
        "12345",
        "--max-results",
        "7",
        "--output",
        str(output_path),
    ])

    lines = output_path.read_text(encoding="utf-8").splitlines()
    assert [json.loads(line) for line in lines] == items


def test_aldi_export_requires_zip_code():
    from app.aldi import export

    with pytest.raises(SystemExit):
        export.main(["--max-results", "7"])
