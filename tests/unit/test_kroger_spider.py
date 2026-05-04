import asyncio
import json

import orjson

from app.kroger.spider import KrogerSpider


def _kroger_product(product_id: str):
    return {
        "id": product_id,
        "item": {
            "description": f"Product {product_id}",
            "brand": {"name": "Kroger"},
            "customerFacingSize": "12 oz",
            "seoDescription": f"product-{product_id}",
            "ratingsAndReviewsAggregate": {
                "averageRating": 4.5,
                "numberOfReviews": 12,
            },
            "images": [
                {
                    "perspective": "front",
                    "size": "large",
                    "url": f"https://example.com/{product_id}.jpg",
                }
            ],
        },
        "price": {
            "storePrices": {
                "regular": {
                    "price": "$3.49",
                    "defaultDescription": "$3.49",
                    "equivalizedUnitPriceString": "$0.29/oz",
                },
                "promo": {"defaultDescription": "2 for $6"},
            }
        },
        "inventory": {"locations": [{"stockLevel": "HIGH"}]},
    }


def _initial_state_html(products):
    state = {
        "calypso": {
            "useCases": {
                "getProducts": {
                    "search-grid": {
                        "response": {
                            "data": {
                                "products": products,
                            }
                        }
                    }
                }
            }
        }
    }
    state_json = orjson.dumps(state).decode().replace("'", "\\'")
    return f"<script>window.__INITIAL_STATE__ = JSON.parse('{state_json}')</script>"


async def _collect_parse(spider, page):
    results = []
    async for item in spider.parse(page):
        results.append(item)
    return results


class TestKrogerSpider:
    def test_parse_returns_normalized_products(self, mock_page_factory):
        spider = KrogerSpider(["milk"], "014003", max_results=10)
        page = mock_page_factory(
            status=200,
            body=_initial_state_html([_kroger_product("000111")]),
            url="https://www.kroger.com/search?query=milk&searchType=default_search",
        )
        page.meta = {"query": "milk"}

        results = asyncio.run(_collect_parse(spider, page))

        assert len(results) == 1
        product = results[0]
        assert product["retailer"] == "kroger"
        assert product["query"] == "milk"
        assert product["location_id"] == "014003"
        assert product["name"] == "Product 000111"
        assert product["price"] == 3.49
        assert product["price_display"] == "$3.49"
        assert product["image_url"] == "https://example.com/000111.jpg"
        assert product["availability"] == "HIGH"
        assert product["url"] == "https://www.kroger.com/p/product-000111/000111"

    def test_parse_respects_max_results(self, mock_page_factory):
        spider = KrogerSpider(["eggs"], "014003", max_results=3)
        products = [_kroger_product(str(i)) for i in range(10)]
        page = mock_page_factory(status=200, body=_initial_state_html(products))
        page.meta = {"query": "eggs"}

        results = asyncio.run(_collect_parse(spider, page))

        assert len(results) == 3
        assert [item["product_id"] for item in results] == ["0", "1", "2"]

    def test_parse_skips_non_200_without_crashing(self, mock_page_factory):
        spider = KrogerSpider(["bread"], "014003", max_results=10)
        page = mock_page_factory(status=503, body="Service unavailable")
        page.meta = {"query": "bread"}

        results = asyncio.run(_collect_parse(spider, page))

        assert results == []

    def test_is_blocked_detects_block_status(self, mock_page_factory):
        spider = KrogerSpider(["bread"], "014003", max_results=10)
        page = mock_page_factory(status=429, body="Too many requests")

        assert asyncio.run(spider.is_blocked(page)) is True


def test_kroger_export_writes_jsonl(monkeypatch, tmp_path):
    from app.kroger import export

    output_path = tmp_path / "kroger_products.jsonl"
    items = [
        {"retailer": "kroger", "name": "Milk", "query": "milk"},
        {"retailer": "kroger", "name": "Eggs", "query": "eggs"},
    ]

    def fake_run_kroger_batch(queries, location_id, max_results):
        assert len(queries) == 25
        assert location_id == "014003"
        assert max_results == 7
        return items

    monkeypatch.setattr(export, "run_kroger_batch", fake_run_kroger_batch)

    export.main(["--location-id", "014003", "--max-results", "7", "--output", str(output_path)])

    lines = output_path.read_text(encoding="utf-8").splitlines()
    assert [json.loads(line) for line in lines] == items
