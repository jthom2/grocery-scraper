# validates walmart search handles various api response shapes
import orjson

import pytest

from app.walmart.search_products import search


# verifies search extraction and normalization logic
class TestWalmartSearch:
    # builds realistic html for mocking walmart responses
    def _create_next_data_html(self, items):
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

    # ensures pydantic model is applied to search results
    def test_search_returns_normalized_products(self, mock_fetcher, mock_page_factory):
        items = [
            {
                "usItemId": "123456",
                "name": "Test Product",
                "brand": "TestBrand",
                "price": 9.99,
                "priceInfo": {"linePriceDisplay": "$9.99"},
                "rating": {"averageRating": 4.5, "numberOfReviews": 100},
                "availabilityStatusV2": {"value": "IN_STOCK"},
                "canonicalUrl": "/ip/test-product/123456",
                "__typename": "SearchProduct",
            }
        ]
        html = self._create_next_data_html(items)
        mock_fetcher.return_value = mock_page_factory(body=html)

        results = search("test query")

        assert len(results) == 1
        product = results[0]
        assert product["retailer"] == "walmart"
        assert product["product_id"] == "123456"
        assert product["name"] == "Test Product"
        assert product["price"] == 9.99

    # placeholders pollute results if not filtered
    def test_search_skips_placeholder_products(self, mock_fetcher, mock_page_factory):
        items = [
            {
                "usItemId": "123456",
                "name": "Real Product",
                "price": 9.99,
                "__typename": "SearchProduct",
            },
            {
                "usItemId": None,
                "name": None,
                "__typename": "SearchPlaceholderProduct",
            },
        ]
        html = self._create_next_data_html(items)
        mock_fetcher.return_value = mock_page_factory(body=html)

        results = search("test query")

        assert len(results) == 1
        assert results[0]["product_id"] == "123456"

    # nameless items break normalization and display
    def test_search_skips_items_without_name(self, mock_fetcher, mock_page_factory):
        items = [
            {
                "usItemId": "123456",
                "name": "Valid Product",
                "price": 9.99,
            },
            {
                "usItemId": "789",
                "name": None,
                "price": 4.99,
            },
            {
                "usItemId": "101112",
                # no name key at all
                "price": 2.99,
            },
        ]
        html = self._create_next_data_html(items)
        mock_fetcher.return_value = mock_page_factory(body=html)

        results = search("test query")

        assert len(results) == 1
        assert results[0]["name"] == "Valid Product"

    # prevents excessive memory use and response time
    def test_search_respects_max_results(self, mock_fetcher, mock_page_factory):
        items = [
            {"usItemId": str(i), "name": f"Product {i}", "price": i * 1.0}
            for i in range(10)
        ]
        html = self._create_next_data_html(items)
        mock_fetcher.return_value = mock_page_factory(body=html)

        results = search("test", max_results=3)

        assert len(results) == 3

    # store-scoped search should hide products unavailable at that store
    def test_search_with_cookies_filters_by_store(self, mock_fetcher, mock_page_factory):
        items = [
            {
                "usItemId": "available",
                "name": "Available Product",
                "price": 5.0,
                "fulfillmentSummary": [{"storeId": "123"}],
            },
            {
                "usItemId": "unavailable",
                "name": "Unavailable Product",
                "price": 10.0,
                "fulfillmentSummary": [{"storeId": "999"}],
            },
        ]
        html = self._create_next_data_html(items)
        mock_fetcher.return_value = mock_page_factory(body=html)

        cookies = {"assortmentStoreId": "123"}
        results = search("test", cookies=cookies)

        assert len(results) == 1
        assert results[0]["product_id"] == "available"

    # regression test for field extraction after api changes
    def test_search_extracts_all_fields(self, mock_fetcher, mock_page_factory):
        items = [
            {
                "usItemId": "PROD123",
                "name": "Full Product",
                "brand": "BrandName",
                "salesUnit": "16 oz",
                "price": 12.99,
                "priceInfo": {
                    "linePriceDisplay": "$12.99",
                    "unitPrice": "$0.81/oz",
                    "wasPrice": "$14.99",
                },
                "rating": {"averageRating": 4.2, "numberOfReviews": 500},
                "availabilityStatusV2": {"value": "IN_STOCK", "display": "In stock"},
                "image": {"url": "https://example.com/image.jpg"},
                "canonicalUrl": "/ip/full-product/PROD123",
                "shortDescription": "A great product",
            }
        ]
        html = self._create_next_data_html(items)
        mock_fetcher.return_value = mock_page_factory(body=html)

        results = search("test")

        product = results[0]
        assert product["product_id"] == "PROD123"
        assert product["brand"] == "BrandName"
        assert product["size"] == "16 oz"
        assert product["price"] == 12.99
        assert product["price_display"] == "$12.99"
        assert product["unit_price"] == "$0.81/oz"
        assert product["rating"] == 4.2
        assert product["reviews"] == 500
        assert product["in_stock"] is True
        assert product["availability"] == "In stock"
        assert product["image_url"] == "https://example.com/image.jpg"
        assert "full-product" in product["url"]

    # walmart api sometimes returns string instead of {url: ...}
    def test_search_handles_image_as_string(self, mock_fetcher, mock_page_factory):
        items = [
            {
                "usItemId": "123",
                "name": "Product",
                "image": "https://example.com/image.jpg",
            }
        ]
        html = self._create_next_data_html(items)
        mock_fetcher.return_value = mock_page_factory(body=html)

        results = search("test")

        assert results[0]["image_url"] == "https://example.com/image.jpg"

    # empty results should not raise exceptions
    def test_search_handles_empty_item_stacks(self, mock_fetcher, mock_page_factory):
        html = self._create_next_data_html([])
        mock_fetcher.return_value = mock_page_factory(body=html)

        results = search("test")

        assert results == []
