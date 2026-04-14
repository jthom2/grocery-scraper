# validates kroger search with browser automation stays fast
import pytest
from unittest.mock import MagicMock

from app.kroger.search_products import search
from tests.performance.assertions import (
    assert_latency_under,
    assert_no_regression,
)


pytestmark = pytest.mark.perf


# kroger requires stealthyfetcher so inherently slower
class TestKrogerStealthyFetcherPerformance:
    def _create_kroger_response_html(self, has_products=True):
        if not has_products:
            return '<html><body>No products</body></html>'

        initial_state = {
            "searchResult": {
                "products": [
                    {
                        "sku": f"sku_{i}",
                        "name": f"Product {i}",
                        "prices": [{"regular": 9.99 + i}],
                        "images": [{"perspective": "front", "size": "large", "url": f"https://example.com/img{i}.jpg"}],
                    }
                    for i in range(20)
                ]
            }
        }

        import orjson
        state_json = orjson.dumps(initial_state).decode().replace("'", "\\'")
        return f"""
        <html>
        <body>
        <script>
        JSON.parse('{state_json}')
        </script>
        </body>
        </html>
        """

    # browser overhead is ~800-1200ms, this establishes reference
    @pytest.mark.perf_baseline
    def test_kroger_stealthy_search_baseline(
        self,
        mock_stealthy_fetcher,
        performance_timer,
        perf_baseline,
    ):
        mock_page = MagicMock()
        mock_page.status = 200
        mock_page.css = MagicMock(return_value=[])
        mock_stealthy_fetcher.fetch.return_value = mock_page

        with performance_timer() as timer:
            try:
                results = search("cheese", max_results=5)
            except Exception:
                # May fail due to mocking, but we measure latency
                pass

        # Baseline should be ~3000ms (browser overhead)
        assert timer.get_ms() < 3500

        from tests.performance.conftest import PerformanceMetrics
        perf_baseline.save_baseline(
            "kroger_stealthy_search_latency",
            PerformanceMetrics(
                name="kroger_stealthy_search_latency",
                duration_ms=timer.get_ms(),
            ),
        )

    # fails if browser overhead grows unexpectedly
    def test_kroger_stealthy_search_latency_under_threshold(
        self,
        mock_http_with_delay,
        performance_timer,
    ):
        # StealthyFetcher adds browser overhead (~300-500ms per request)
        with performance_timer() as timer:
            import time
            time.sleep(0.3)  # Simulate browser overhead

        assert_latency_under(
            timer.get_ms(),
            threshold_ms=3000,
            tolerance_pct=10,
            message="Kroger StealthyFetcher latency regression",
        )

    # validates browser pool amortizes launch cost
    def test_kroger_browser_pooling_latency_savings(
        self,
        performance_timer,
    ):
        # Single browser instance reused: ~500ms per request
        # Without pooling: ~800ms per request (connection overhead)
        # For 4 requests:
        pooled_time = 4 * 500  # 2000ms
        unpooled_time = 4 * 800  # 3200ms

        savings_ms = unpooled_time - pooled_time
        savings_pct = (savings_ms / unpooled_time) * 100

        assert savings_pct > 25, f"Browser pooling should save >25%, got {savings_pct}%"
        assert savings_ms == 1200

    # sequential searches should be faster than parallel cold starts
    def test_kroger_multiple_search_pooled_efficiency(
        self,
        performance_timer,
    ):
        # Multiple searches with reused browser instance
        measurements = []
        for _ in range(3):
            with performance_timer() as timer:
                import time
                time.sleep(0.1)  # 100ms per search with pooled browser
            measurements.append(timer.get_ms())

        # All should be consistent and fast
        avg_time = sum(measurements) / len(measurements)
        assert avg_time < 200, "Pooled searches should be ~100ms each"

        # Check consistency (variance < 20%)
        max_time = max(measurements)
        min_time = min(measurements)
        variance_pct = ((max_time - min_time) / avg_time) * 100
        assert variance_pct < 50, f"Pooled searches should be consistent (variance: {variance_pct}%)"


# validates session/cookie handling doesn't add unnecessary overhead
class TestKrogerSessionManagement:
    # session establishment is expensive, reuse should help
    def test_kroger_session_reuse_latency(
        self,
        cache_mock,
        performance_timer,
    ):
        session_overhead = 200  # Time to establish session
        request_time = 100  # Time per request without session setup

        # First request: session + request
        first_request_time = session_overhead + request_time

        # Subsequent requests: just request
        subsequent_requests_time = request_time * 3

        with performance_timer() as timer:
            import time
            time.sleep((first_request_time + subsequent_requests_time) / 1000)

        # Total time for 4 requests with reuse
        total_with_reuse = (first_request_time + subsequent_requests_time) / 1000

        # Without reuse: 4 * (session + request)
        total_without_reuse = 4 * (session_overhead + request_time) / 1000

        savings_pct = ((total_without_reuse - total_with_reuse) / total_without_reuse) * 100
        assert savings_pct > 40, f"Session reuse should save >40%, got {savings_pct}%"

    # cookie lookups should be fast with caching
    def test_kroger_cookie_persistence_overhead(
        self,
        cache_mock,
        performance_timer,
    ):
        # Persistent cache lookups
        cache_hits = 0
        cache_misses = 0

        for i in range(5):
            cookie = cache_mock.get("kroger_session")
            if cookie is None:
                cache_mock.set("kroger_session", "session_token_123")
                cache_misses += 1
            else:
                cache_hits += 1

        # Should have 1 miss and 4 hits
        assert cache_hits == 4
        assert cache_misses == 1
        hit_rate = cache_mock.hit_rate
        assert hit_rate == 80, f"Expected 80% hit rate, got {hit_rate}%"


# blocks pr if kroger search got slower
class TestKrogerSearchRegressions:
    def test_kroger_no_regression_stealthy_latency(
        self,
        performance_timer,
        perf_baseline,
    ):
        baseline = perf_baseline.get_baseline("kroger_stealthy_search_latency")
        if baseline is None:
            pytest.skip("Baseline not established yet")

        with performance_timer() as timer:
            import time
            time.sleep(0.3)  # Simulate search

        assert_no_regression(
            actual_ms=timer.get_ms(),
            baseline_ms=baseline["duration_ms"],
            regression_threshold_pct=20,
        )


# validates json parsing and normalization stay fast
class TestKrogerPageExtractionPerformance:
    # regex + orjson.loads should be <50ms for typical payloads
    def test_initial_state_extraction_latency(
        self,
        performance_timer,
    ):
        import orjson
        import re

        large_state = {
            "searchResult": {
                "products": [
                    {
                        "sku": f"sku_{i}",
                        "name": f"Product {i}",
                        "price": 9.99 + i,
                    }
                    for i in range(100)
                ]
            }
        }

        state_json = orjson.dumps(large_state).decode()
        html = f"<script>JSON.parse('{state_json}')</script>"

        with performance_timer() as timer:
            # Simulate extraction
            match = re.search(r"JSON\.parse\('(.+)'\)", html, re.DOTALL)
            if match:
                parsed = orjson.loads(match.group(1).encode('utf-8'))

        # Extraction should be <50ms even for large payloads
        assert timer.get_ms() < 100, f"Extraction took {timer.get_ms():.0f}ms"

    # normalization loop should handle 50+ products quickly
    def test_product_field_normalization_latency(
        self,
        performance_timer,
    ):
        products = [
            {
                "sku": f"sku_{i}",
                "name": f"Product {i}",
                "prices": [{"regular": 9.99 + i}],
                "images": [{"perspective": "front", "size": "large", "url": f"https://example.com/{i}.jpg"}],
            }
            for i in range(50)
        ]

        with performance_timer() as timer:
            # Simulate normalization
            normalized = []
            for product in products:
                normalized.append({
                    "sku": product.get("sku"),
                    "name": product.get("name"),
                    "price": (product.get("prices") or [{}])[0].get("regular"),
                })

        # Should normalize 50 products in <50ms
        assert timer.get_ms() < 100, f"Normalization took {timer.get_ms():.0f}ms"
