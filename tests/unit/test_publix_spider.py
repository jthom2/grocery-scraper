import asyncio
import json

from app.publix.spider import PublixSpider


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


def _publix_html(count: int = 1):
    links = []
    for index in range(count):
        product_id = f"RIO-PCI-{index + 111}"
        slug = f"product-{index + 1}"
        price = f"${index + 3}.49"
        links.append(
            f'<a href="/pd/{slug}/{product_id}" aria-label="{price} - Product {index + 1}">Link</a>'
        )
    return f"<html><body>{''.join(links)}</body></html>"


class TestPublixSpider:
    def test_parse_returns_normalized_products(self, mock_page_factory):
        spider = PublixSpider(["milk"], "1234", max_results=10)
        page = mock_page_factory(
            status=200,
            body=_publix_html(1),
            url="https://www.publix.com/search?searchTerm=milk&facet=promoType%3A%3Atrue",
        )
        page.meta = {"query": "milk"}

        results = asyncio.run(_collect_parse(spider, page))

        assert len(results) == 1
        product = results[0]
        assert product["retailer"] == "publix"
        assert product["query"] == "milk"
        assert product["location_id"] == "1234"
        assert product["name"] == "Product 1"
        assert product["price"] == 3.49
        assert product["price_display"] == "$3.49"
        assert product["product_id"] == "RIO-PCI-111"
        assert product["url"] == "https://www.publix.com/pd/product-1/RIO-PCI-111"

    def test_parse_respects_max_results(self, mock_page_factory):
        spider = PublixSpider(["eggs"], "1234", max_results=3)
        page = mock_page_factory(status=200, body=_publix_html(10))
        page.meta = {"query": "eggs"}

        results = asyncio.run(_collect_parse(spider, page))

        assert len(results) == 3
        assert [item["product_id"] for item in results] == [
            "RIO-PCI-111",
            "RIO-PCI-112",
            "RIO-PCI-113",
        ]

    def test_parse_skips_non_200_without_crashing(self, mock_page_factory):
        spider = PublixSpider(["bread"], "1234", max_results=10)
        page = mock_page_factory(status=503, body="Service unavailable")
        page.meta = {"query": "bread"}

        results = asyncio.run(_collect_parse(spider, page))

        assert results == []

    def test_is_blocked_detects_block_status(self, mock_page_factory):
        spider = PublixSpider(["bread"], "1234", max_results=10)
        page = mock_page_factory(status=429, body="Too many requests")

        assert asyncio.run(spider.is_blocked(page)) is True

    def test_start_requests_builds_encoded_urls_and_store_cookie(self):
        spider = PublixSpider(["chicken breast"], "1234", max_results=10)

        requests = asyncio.run(_collect_start_requests(spider))

        assert len(requests) == 1
        assert requests[0].url == (
            "https://www.publix.com/search?searchTerm=chicken%20breast&facet=promoType%3A%3Atrue"
        )
        assert requests[0].meta == {"query": "chicken breast"}
        assert spider.cookie_dict == {"Store": '{"storeNumber":"1234"}'}
        assert spider.cookies == [
            {"name": "Store", "value": '{"storeNumber":"1234"}', "url": "https://www.publix.com/"}
        ]


def test_publix_export_writes_jsonl(monkeypatch, tmp_path):
    from app.publix import export

    output_path = tmp_path / "publix_products.jsonl"
    items = [
        {"retailer": "publix", "name": "Milk", "query": "milk"},
        {"retailer": "publix", "name": "Eggs", "query": "eggs"},
    ]

    def fake_run_publix_batch(queries, location_id, max_results):
        assert len(queries) == 25
        assert location_id == "1234"
        assert max_results == 7
        return items

    monkeypatch.setattr(export, "run_publix_batch", fake_run_publix_batch)

    export.main(["--location-id", "1234", "--max-results", "7", "--output", str(output_path)])

    lines = output_path.read_text(encoding="utf-8").splitlines()
    assert [json.loads(line) for line in lines] == items
