import orjson
import re
from pathlib import Path
from unittest.mock import MagicMock

import pytest

FIXTURES_DIR = Path(__file__).parent / "fixtures"


# mimics scrapling response for tests without network calls
class MockPage:
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
        return orjson.loads(self.body)

    # parses script tags from html body to support search extraction tests
    def css(self, selector: str):
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


# simple text container for css selector results
class MockElement:
    def __init__(self, text: str = ""):
        self.text = text


# loads test data files from fixtures directory
@pytest.fixture
def load_fixture():
    def _load(relative_path: str) -> str | dict:
        fixture_path = FIXTURES_DIR / relative_path
        if fixture_path.suffix == ".json":
            return orjson.loads(fixture_path.read_bytes())
        return fixture_path.read_text(encoding="utf-8")

    return _load


# returns class for tests to instantiate with custom params
@pytest.fixture
def mock_page_factory():
    return MockPage


# patches http fetcher at app level for search tests
@pytest.fixture
def mock_fetcher(mocker):
    return mocker.patch("app.utils.fetcher.fetch")


# patches at scrapling level when app-level patch is insufficient
@pytest.fixture
def mock_scrapling_fetcher(mocker):
    return mocker.patch("scrapling.fetchers.Fetcher.get")


# avoids browser launch overhead in unit tests
@pytest.fixture
def mock_stealthy_fetcher(mocker):
    mock_sf_class = mocker.patch("scrapling.StealthyFetcher")
    mock_sf_instance = MagicMock()
    mock_sf_class.return_value = mock_sf_instance
    return mock_sf_instance


# clears lru_cache to prevent cross-test pollution
@pytest.fixture
def mock_requests_get(mocker):
    from app.utils.zip2loc import _ZIP_CACHE, _fetch_from_api
    from app.aldi.search_products import get_coordinates

    _ZIP_CACHE.clear()  # clear TTL cache
    _fetch_from_api.cache_clear()  # clear lru_cache on the fetch function
    get_coordinates.cache_clear()

    return mocker.patch("requests.get")


# minimal fields to pass pydantic validation
@pytest.fixture
def sample_product_data():
    return {
        "retailer": "walmart",
        "product_id": "123456",
        "name": "Test Product",
        "price": 9.99,
    }


# minimal fields to pass pydantic validation
@pytest.fixture
def sample_location_data():
    return {
        "retailer": "walmart",
        "location_id": "5678",
        "name": "Test Store",
    }


# shared across retailer price extraction tests
@pytest.fixture
def price_extraction_cases():
    return [
        (None, None),
        (9.99, 9.99),
        (10, 10.0),
        ("9.99", 9.99),
        ("$9.99", 9.99),
        ("USD 2.79", 2.79),
        ("", None),
    ]
