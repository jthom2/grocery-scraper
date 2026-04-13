import json
import re
from pathlib import Path
from unittest.mock import MagicMock

import pytest

FIXTURES_DIR = Path(__file__).parent / "fixtures"


class MockPage:
    """Mock scrapling page response object."""

    def __init__(
        self,
        status: int = 200,
        body: str = "",
        url: str = "https://example.com",
        cookies: dict | None = None,
        headers: dict | None = None,
        json_data: dict | None = None,
    ):
        self.status = status
        self.body = body
        self.url = url
        self.cookies = cookies or {}
        self.headers = headers or {}
        self._json_data = json_data

    def json(self):
        if self._json_data is not None:
            return self._json_data
        return json.loads(self.body)

    def css(self, selector: str):
        """Mock CSS selector - returns list of MockElement."""
        if selector == "script#__NEXT_DATA__":
            match = re.search(
                r'<script id="__NEXT_DATA__"[^>]*>(.*?)</script>',
                self.body,
                re.DOTALL,
            )
            if match:
                return [MockElement(text=match.group(1))]
            return []

        if selector == "script":
            scripts = re.findall(r"<script[^>]*>(.*?)</script>", self.body, re.DOTALL)
            return [MockElement(text=s) for s in scripts]

        return []


class MockElement:
    """Mock HTML element."""

    def __init__(self, text: str = ""):
        self.text = text


@pytest.fixture
def load_fixture():
    """Factory fixture to load JSON/HTML fixtures by path."""

    def _load(relative_path: str) -> str | dict:
        fixture_path = FIXTURES_DIR / relative_path
        content = fixture_path.read_text(encoding="utf-8")
        if fixture_path.suffix == ".json":
            return json.loads(content)
        return content

    return _load


@pytest.fixture
def mock_page_factory():
    """Factory to create MockPage instances."""
    return MockPage


@pytest.fixture
def mock_fetcher(mocker):
    """Mock app.utils.fetcher.fetch to return MockPage instances."""
    return mocker.patch("app.utils.fetcher.fetch")


@pytest.fixture
def mock_scrapling_fetcher(mocker):
    """Mock scrapling.fetchers.Fetcher.get directly."""
    return mocker.patch("scrapling.fetchers.Fetcher.get")


@pytest.fixture
def mock_stealthy_fetcher(mocker):
    """Mock scrapling.StealthyFetcher for browser automation tests."""
    mock_sf_class = mocker.patch("scrapling.StealthyFetcher")
    mock_sf_instance = MagicMock()
    mock_sf_class.return_value = mock_sf_instance
    return mock_sf_instance


@pytest.fixture
def mock_requests_get(mocker):
    """Mock requests.get for utilities using requests directly."""
    return mocker.patch("requests.get")


@pytest.fixture
def sample_product_data():
    """Minimal valid product data for normalization."""
    return {
        "retailer": "walmart",
        "product_id": "123456",
        "name": "Test Product",
        "price": 9.99,
    }


@pytest.fixture
def sample_location_data():
    """Minimal valid location data for normalization."""
    return {
        "retailer": "walmart",
        "location_id": "5678",
        "name": "Test Store",
    }


@pytest.fixture
def price_extraction_cases():
    """Common test cases for price extraction functions."""
    return [
        (None, None),
        (9.99, 9.99),
        (10, 10.0),
        ("9.99", 9.99),
        ("$9.99", 9.99),
        ("USD 2.79", 2.79),
        ("", None),
    ]
