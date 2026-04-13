"""Performance test fixtures and configuration."""
import json
import time
from pathlib import Path
from unittest.mock import MagicMock
from dataclasses import dataclass, asdict
from typing import Optional

import pytest


PERF_BASELINES_DIR = Path(__file__).parent / "baselines"
PERF_BASELINES_DIR.mkdir(exist_ok=True)


@dataclass
class PerformanceMetrics:
    """Container for performance measurements."""
    name: str
    duration_ms: float
    cache_hits: int = 0
    cache_misses: int = 0
    total_requests: int = 1
    timestamp: str = ""

    def to_dict(self) -> dict:
        """Convert to serializable dict."""
        return asdict(self)

    @property
    def cache_hit_rate(self) -> float:
        """Calculate cache hit rate as percentage."""
        total = self.cache_hits + self.cache_misses
        if total == 0:
            return 0.0
        return (self.cache_hits / total) * 100


class PerformanceBaseline:
    """Manages performance baselines for regression tracking."""

    def __init__(self, baseline_file: Optional[Path] = None):
        """Initialize baseline manager.

        Args:
            baseline_file: Path to baseline JSON file. Defaults to
                          baselines/performance.json
        """
        self.baseline_file = baseline_file or PERF_BASELINES_DIR / "performance.json"
        self._load_baselines()

    def _load_baselines(self):
        """Load baselines from JSON file."""
        self.baselines = {}
        if self.baseline_file.exists():
            try:
                self.baselines = json.loads(self.baseline_file.read_text())
            except (json.JSONDecodeError, IOError):
                pass

    def get_baseline(self, test_name: str) -> Optional[dict]:
        """Retrieve baseline for a test.

        Args:
            test_name: Identifier for the test/measurement

        Returns:
            Baseline dict or None if not found
        """
        return self.baselines.get(test_name)

    def save_baseline(self, test_name: str, metrics: PerformanceMetrics):
        """Save baseline metrics.

        Args:
            test_name: Identifier for the test/measurement
            metrics: PerformanceMetrics instance to save
        """
        metrics.timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        self.baselines[test_name] = metrics.to_dict()
        self.baseline_file.write_text(
            json.dumps(self.baselines, indent=2)
        )

    def get_all_baselines(self) -> dict:
        """Get all stored baselines."""
        return self.baselines.copy()


@pytest.fixture
def perf_baseline():
    """Provide performance baseline manager."""
    return PerformanceBaseline()


@pytest.fixture
def performance_timer():
    """Provide a simple timer context manager for measuring performance."""

    class Timer:
        """Simple timer for measuring elapsed time."""

        def __init__(self):
            self.start_time = None
            self.elapsed_ms = 0.0

        def __enter__(self):
            self.start_time = time.perf_counter()
            return self

        def __exit__(self, *args):
            self.elapsed_ms = (time.perf_counter() - self.start_time) * 1000

        def get_ms(self) -> float:
            """Get elapsed time in milliseconds."""
            return self.elapsed_ms

    return Timer


@pytest.fixture
def mock_http_with_delay(mocker):
    """Mock HTTP fetcher that simulates realistic network delays.

    Returns a factory function that creates mocked responses with
    configurable delays to simulate real network conditions.
    """

    def _mock_fetch_with_delay(delay_ms: float, status: int = 200, body: str = ""):
        """Create a mocked fetch function with delay.

        Args:
            delay_ms: Simulated network delay in milliseconds
            status: HTTP status code (default 200)
            body: Response body content

        Returns:
            Function that can be used as mock for fetcher.fetch
        """

        def mock_fetch(*args, **kwargs):
            time.sleep(delay_ms / 1000)
            mock_response = MagicMock()
            mock_response.status = status
            mock_response.body = body
            mock_response.url = kwargs.get("url", "https://example.com")
            mock_response.cookies = {}
            mock_response.headers = {}
            return mock_response

        return mock_fetch

    return _mock_fetch_with_delay


@pytest.fixture
def cache_mock():
    """Provide a mock cache with hit/miss tracking."""

    class MockCache:
        """Cache mock with statistics tracking."""

        def __init__(self):
            self.data = {}
            self.hits = 0
            self.misses = 0

        def get(self, key: str, default=None):
            """Get value from cache with hit/miss tracking."""
            if key in self.data:
                self.hits += 1
                return self.data[key]
            self.misses += 1
            return default

        def set(self, key: str, value):
            """Set value in cache."""
            self.data[key] = value

        def clear(self):
            """Clear cache and reset stats."""
            self.data.clear()
            self.hits = 0
            self.misses = 0

        @property
        def hit_rate(self) -> float:
            """Get hit rate as percentage."""
            total = self.hits + self.misses
            if total == 0:
                return 0.0
            return (self.hits / total) * 100

        @property
        def stats(self) -> dict:
            """Get cache statistics."""
            return {
                "hits": self.hits,
                "misses": self.misses,
                "hit_rate": self.hit_rate,
                "size": len(self.data),
            }

    return MockCache()


@pytest.fixture
def mock_request_tracker():
    """Track HTTP requests for performance analysis."""

    class RequestTracker:
        """Track and profile HTTP requests."""

        def __init__(self):
            self.requests = []
            self.total_time = 0.0

        def add_request(self, url: str, duration_ms: float):
            """Record a request.

            Args:
                url: Request URL
                duration_ms: Request duration in milliseconds
            """
            self.requests.append({
                "url": url,
                "duration_ms": duration_ms,
            })
            self.total_time += duration_ms

        def get_slowest_requests(self, n: int = 5) -> list:
            """Get slowest requests.

            Args:
                n: Number of slowest requests to return

            Returns:
                List of slowest request dicts, ordered by duration descending
            """
            return sorted(
                self.requests,
                key=lambda r: r["duration_ms"],
                reverse=True,
            )[:n]

        def get_stats(self) -> dict:
            """Get request statistics."""
            if not self.requests:
                return {
                    "total_requests": 0,
                    "total_time_ms": 0.0,
                    "avg_time_ms": 0.0,
                }

            avg = self.total_time / len(self.requests)
            return {
                "total_requests": len(self.requests),
                "total_time_ms": self.total_time,
                "avg_time_ms": avg,
                "slowest_requests": self.get_slowest_requests(3),
            }

        def reset(self):
            """Clear all tracked requests."""
            self.requests.clear()
            self.total_time = 0.0

    return RequestTracker()
