# fixtures for measuring and tracking performance regressions
import orjson
import time
from pathlib import Path
from unittest.mock import MagicMock
from dataclasses import dataclass, asdict
from typing import Optional

import pytest


PERF_BASELINES_DIR = Path(__file__).parent / "baselines"
PERF_BASELINES_DIR.mkdir(exist_ok=True)


# holds timing and cache stats for a single test run
@dataclass
class PerformanceMetrics:
    name: str
    duration_ms: float
    cache_hits: int = 0
    cache_misses: int = 0
    total_requests: int = 1
    timestamp: str = ""

    def to_dict(self) -> dict:
        return asdict(self)

    @property
    def cache_hit_rate(self) -> float:
        total = self.cache_hits + self.cache_misses
        if total == 0:
            return 0.0
        return (self.cache_hits / total) * 100


# stores and retrieves baseline metrics for comparison
class PerformanceBaseline:
    def __init__(self, baseline_file: Optional[Path] = None):
        self.baseline_file = baseline_file or PERF_BASELINES_DIR / "performance.json"
        self._load_baselines()

    def _load_baselines(self):
        self.baselines = {}
        if self.baseline_file.exists():
            try:
                self.baselines = orjson.loads(self.baseline_file.read_bytes())
            except (orjson.JSONDecodeError, IOError):
                pass

    def get_baseline(self, test_name: str) -> Optional[dict]:
        return self.baselines.get(test_name)

    def save_baseline(self, test_name: str, metrics: PerformanceMetrics):
        metrics.timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        self.baselines[test_name] = metrics.to_dict()
        self.baseline_file.write_bytes(
            orjson.dumps(self.baselines, option=orjson.OPT_INDENT_2)
        )

    def get_all_baselines(self) -> dict:
        return self.baselines.copy()


# provides access to stored baselines for comparison
@pytest.fixture
def perf_baseline():
    return PerformanceBaseline()


# context manager for timing code blocks
@pytest.fixture
def performance_timer():
    class Timer:
        def __init__(self):
            self.start_time = None
            self.elapsed_ms = 0.0

        def __enter__(self):
            self.start_time = time.perf_counter()
            return self

        def __exit__(self, *args):
            self.elapsed_ms = (time.perf_counter() - self.start_time) * 1000

        def get_ms(self) -> float:
            return self.elapsed_ms

    return Timer


# simulates network latency in unit tests
@pytest.fixture
def mock_http_with_delay():
    def _mock_fetch_with_delay(delay_ms: float, status: int = 200, body: str = ""):
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


# tracks cache operations for verifying caching works
@pytest.fixture
def cache_mock():
    class MockCache:
        def __init__(self):
            self.data = {}
            self.hits = 0
            self.misses = 0

        def get(self, key: str, default=None):
            if key in self.data:
                self.hits += 1
                return self.data[key]
            self.misses += 1
            return default

        def set(self, key: str, value):
            self.data[key] = value

        def clear(self):
            self.data.clear()
            self.hits = 0
            self.misses = 0

        @property
        def hit_rate(self) -> float:
            total = self.hits + self.misses
            if total == 0:
                return 0.0
            return (self.hits / total) * 100

        @property
        def stats(self) -> dict:
            return {
                "hits": self.hits,
                "misses": self.misses,
                "hit_rate": self.hit_rate,
                "size": len(self.data),
            }

    return MockCache()


# counts and times requests for detecting request bloat
@pytest.fixture
def mock_request_tracker():
    class RequestTracker:
        def __init__(self):
            self.requests = []
            self.total_time = 0.0

        def add_request(self, url: str, duration_ms: float):
            self.requests.append({
                "url": url,
                "duration_ms": duration_ms,
            })
            self.total_time += duration_ms

        def get_slowest_requests(self, n: int = 5) -> list:
            return sorted(
                self.requests,
                key=lambda r: r["duration_ms"],
                reverse=True,
            )[:n]

        def get_stats(self) -> dict:
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
            self.requests.clear()
            self.total_time = 0.0

    return RequestTracker()
