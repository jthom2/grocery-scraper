# validates walmart search latency stays within acceptable bounds
try:
    import orjson
except ImportError:
    import json as orjson
import pytest

from app.walmart.search_products import search
from tests.performance.assertions import (
    assert_latency_under,
    assert_no_regression,
)


pytestmark = pytest.mark.perf


# walmart uses simple http fetch, should be fastest retailer
class TestWalmartSearchPerformance:
    # builds html matching walmart's __NEXT_DATA__ structure
    def _create_next_data_html(self, items, count=20):
        next_data = {
            "props": {
                "pageProps": {
                    "initialData": {
                        "searchResult": {
                            "itemStacks": [{"items": items * (count // len(items) + 1)}]
                        }
                    }
                }
            }
        }
        return f'<script id="__NEXT_DATA__">{orjson.dumps(next_data).decode()}</script>'

    def _create_sample_items(self, count=20):
        return [
            {
                "usItemId": f"prod_{i}",
                "name": f"Test Product {i}",
                "brand": "TestBrand",
                "price": 9.99 + i,
                "priceInfo": {"linePriceDisplay": f"${9.99 + i:.2f}"},
                "rating": {"averageRating": 4.5, "numberOfReviews": 100},
                "availabilityStatusV2": {"value": "IN_STOCK"},
                "canonicalUrl": f"/ip/test-product-{i}/{i}",
                "__typename": "SearchProduct",
            }
            for i in range(count)
        ]

    # establishes reference point for regression detection
    @pytest.mark.perf_baseline
    def test_walmart_search_latency_baseline(
        self,
        mock_fetcher,
        mock_page_factory,
        performance_timer,
        perf_baseline,
    ):
        items = self._create_sample_items(count=20)
        html = self._create_next_data_html(items)
        mock_fetcher.return_value = mock_page_factory(body=html)

        with performance_timer() as timer:
            results = search("test query", max_results=5)

        assert len(results) == 5
        assert timer.get_ms() < 700  # Baseline with 50ms tolerance

        from tests.performance.conftest import PerformanceMetrics
        perf_baseline.save_baseline(
            "walmart_search_latency",
            PerformanceMetrics(
                name="walmart_search_latency",
                duration_ms=timer.get_ms(),
            ),
        )

    # fails ci if search slows down
    def test_walmart_search_latency_under_threshold(
        self,
        mock_fetcher,
        mock_page_factory,
        performance_timer,
    ):
        items = self._create_sample_items(count=20)
        html = self._create_next_data_html(items)
        mock_fetcher.return_value = mock_page_factory(body=html)

        with performance_timer() as timer:
            results = search("test query", max_results=5)

        assert len(results) == 5
        assert_latency_under(
            timer.get_ms(),
            threshold_ms=650,
            tolerance_pct=10,
            message="Walmart search latency regression detected",
        )

    # store filtering adds cpu work, verify it stays fast
    def test_walmart_search_with_store_filter_latency(
        self,
        mock_fetcher,
        mock_page_factory,
        performance_timer,
    ):
        items = self._create_sample_items(count=30)
        for i, item in enumerate(items):
            if i % 2 == 0:
                item["fulfillmentSummary"] = [{"storeId": "123"}]
            else:
                item["fulfillmentSummary"] = [{"storeId": "999"}]

        html = self._create_next_data_html(items, count=30)
        mock_fetcher.return_value = mock_page_factory(body=html)

        cookies = {"assortmentStoreId": "123"}

        with performance_timer() as timer:
            results = search("test query", cookies=cookies, max_results=5)

        assert len(results) == 5
        assert_latency_under(timer.get_ms(), threshold_ms=700, tolerance_pct=10)

    # large results shouldn't blow up latency
    def test_walmart_search_large_result_set_latency(
        self,
        mock_fetcher,
        mock_page_factory,
        performance_timer,
    ):
        items = self._create_sample_items(count=100)
        html = self._create_next_data_html(items, count=100)
        mock_fetcher.return_value = mock_page_factory(body=html)

        with performance_timer() as timer:
            results = search("test query", max_results=10)

        assert len(results) == 10
        assert_latency_under(timer.get_ms(), threshold_ms=750, tolerance_pct=10)

    # flaky performance indicates caching or gc issues
    def test_walmart_search_multiple_runs_consistency(
        self,
        mock_fetcher,
        mock_page_factory,
        performance_timer,
    ):
        items = self._create_sample_items(count=20)
        html = self._create_next_data_html(items)
        mock_fetcher.return_value = mock_page_factory(body=html)

        measurements = []
        for _ in range(3):
            with performance_timer() as timer:
                results = search("test query", max_results=5)
            assert len(results) == 5
            measurements.append(timer.get_ms())

        # All runs should be within ~50ms of each other
        max_latency = max(measurements)
        min_latency = min(measurements)
        variance = max_latency - min_latency

        assert variance < 100, (
            f"Search performance inconsistent: "
            f"min={min_latency:.0f}ms, max={max_latency:.0f}ms, "
            f"variance={variance:.0f}ms"
        )


# compares current performance against stored baselines
class TestWalmartSearchRegressions:
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

    def _create_sample_items(self, count=20):
        return [
            {
                "usItemId": f"prod_{i}",
                "name": f"Test Product {i}",
                "price": 9.99 + i,
                "priceInfo": {"linePriceDisplay": f"${9.99 + i:.2f}"},
                "__typename": "SearchProduct",
            }
            for i in range(count)
        ]

    # blocks pr if performance degraded more than 20%
    def test_walmart_no_regression_vs_baseline(
        self,
        mock_fetcher,
        mock_page_factory,
        performance_timer,
        perf_baseline,
    ):
        baseline = perf_baseline.get_baseline("walmart_search_latency")
        if baseline is None:
            pytest.skip("Baseline not established yet")

        items = self._create_sample_items(count=20)
        html = self._create_next_data_html(items)
        mock_fetcher.return_value = mock_page_factory(body=html)

        with performance_timer() as timer:
            results = search("test query", max_results=5)

        assert len(results) == 5
        assert_no_regression(
            actual_ms=timer.get_ms(),
            baseline_ms=baseline["duration_ms"],
            regression_threshold_pct=20,
        )
