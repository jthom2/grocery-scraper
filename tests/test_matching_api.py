from unittest.mock import MagicMock

import pytest
from fastapi.testclient import TestClient

from app.api.dependencies import (
    get_aldi_client,
    get_kroger_client,
    get_publix_client,
    get_walmart_client,
)
from app.api.main import app

client = TestClient(app, raise_server_exceptions=False)


@pytest.fixture
def mock_clients():
    mocks = {
        get_aldi_client: MagicMock(),
        get_kroger_client: MagicMock(),
        get_publix_client: MagicMock(),
        get_walmart_client: MagicMock(),
    }

    def override(mock):
        def _get_mock():
            return mock
        return _get_mock

    for dependency, mock in mocks.items():
        app.dependency_overrides[dependency] = override(mock)

    yield mocks

    for dependency in mocks:
        app.dependency_overrides.pop(dependency, None)


def test_match_search_fetches_multiple_candidates_per_retailer(mock_clients):
    walmart = mock_clients[get_walmart_client]
    kroger = mock_clients[get_kroger_client]
    walmart.build_cookies.return_value = {"w": "v"}
    kroger.build_cookies.return_value = {"k": "v"}
    walmart.search_products.return_value = [
        {
            "retailer": "walmart",
            "product_id": "w1",
            "name": "Great Value 2% Reduced Fat Milk, 1 Gallon",
            "brand": "Great Value",
        }
    ]
    kroger.search_products.return_value = [
        {
            "retailer": "kroger",
            "product_id": "k1",
            "name": "Kroger 2% Reduced Fat Milk, 1 gal",
            "brand": "Kroger",
        }
    ]

    response = client.post(
        "/api/v1/match/search?walmart_location_id=789&kroger_location_id=123",
        json={
            "query": "2% milk 1 gallon",
            "retailers": ["walmart", "kroger"],
            "zip_code": "30303",
            "max_candidates_per_retailer": 3,
        },
    )

    assert response.status_code == 200
    data = response.json()
    assert data["matches_by_retailer"]["walmart"]["status"] == "equivalent"
    assert data["matches_by_retailer"]["kroger"]["status"] == "equivalent"
    assert data["matches_by_retailer"]["walmart"]["best"]["product"]["product_id"] == "w1"
    assert data["matches_by_retailer"]["kroger"]["best"]["product"]["product_id"] == "k1"
    assert data["errors"] == {}
    assert walmart.search_products.call_count == 2
    assert kroger.search_products.call_count == 2
    walmart.search_products.assert_any_call(
        query="2% milk 1 gallon",
        location_id="789",
        max_results=8,
        cookies={"w": "v"},
    )
    walmart.search_products.assert_any_call(
        query="milk 1 gallon",
        location_id="789",
        max_results=8,
        cookies={"w": "v"},
    )
    kroger.search_products.assert_any_call(
        query="2% milk 1 gallon",
        location_id="123",
        max_results=8,
        cookies={"k": "v"},
    )
    kroger.search_products.assert_any_call(
        query="milk 1 gallon",
        location_id="123",
        max_results=8,
        cookies={"k": "v"},
    )


def test_match_search_returns_retailer_errors_without_failing(mock_clients):
    walmart = mock_clients[get_walmart_client]
    kroger = mock_clients[get_kroger_client]
    walmart.search_products.side_effect = Exception("blocked")
    kroger.search_products.return_value = [
        {
            "retailer": "kroger",
            "product_id": "k1",
            "name": "Kroger 2% Reduced Fat Milk, 1 gal",
            "brand": "Kroger",
        }
    ]

    response = client.post("/api/v1/match/search", json={
        "query": "2% milk 1 gallon",
        "retailers": ["walmart", "kroger"],
    })

    assert response.status_code == 200
    data = response.json()
    assert data["errors"] == {"walmart": "unknown_error"}
    assert data["matches_by_retailer"]["walmart"]["status"] == "error"
    assert data["matches_by_retailer"]["walmart"]["error"] == "unknown_error"
    assert data["matches_by_retailer"]["kroger"]["status"] == "equivalent"
    assert data["matches_by_retailer"]["kroger"]["best"]["product"]["product_id"] == "k1"


def test_match_search_sanitizes_browser_runtime_errors(mock_clients):
    walmart = mock_clients[get_walmart_client]
    walmart.search_products.side_effect = Exception(
        "BrowserType.launch_persistent_context: Executable doesn't exist at /tmp/chromium"
    )

    response = client.post("/api/v1/match/search", json={
        "query": "2% milk 1 gallon",
        "retailers": ["walmart"],
    })

    assert response.status_code == 200
    data = response.json()
    assert data["errors"] == {"walmart": "browser_runtime_unavailable"}
    assert "/tmp/chromium" not in str(data)


def test_match_search_groups_no_match_by_retailer(mock_clients):
    aldi = mock_clients[get_aldi_client]
    aldi.search_products.return_value = [
        {
            "retailer": "aldi",
            "product_id": "a1",
            "name": "Barissimo Cinnamon Roll Coffee Creamer",
            "brand": "Barissimo",
            "size": "32 fl oz",
        }
    ]

    response = client.post("/api/v1/match/search", json={
        "query": "2% milk 1 gallon",
        "retailers": ["aldi"],
    })

    assert response.status_code == 200
    data = response.json()
    aldi_group = data["matches_by_retailer"]["aldi"]
    assert aldi_group["status"] == "no_match"
    assert aldi_group["best"] is None
    assert aldi_group["candidates"][0]["decision"] == "different"


def test_match_search_exposes_location_ids_as_query_params():
    schema = client.get("/openapi.json").json()

    post_schema = schema["paths"]["/api/v1/match/search"]["post"]
    parameter_names = {parameter["name"] for parameter in post_schema["parameters"]}
    request_properties = schema["components"]["schemas"]["MatchSearchRequest"]["properties"]
    response_properties = schema["components"]["schemas"]["MatchSearchResponse"]["properties"]

    assert {
        "aldi_location_id",
        "kroger_location_id",
        "publix_location_id",
        "walmart_location_id",
    }.issubset(parameter_names)
    assert "location_ids" not in request_properties
    assert "matches_by_retailer" in response_properties
    assert "equivalent" not in response_properties


def test_existing_unified_search_contract_is_unchanged(mock_clients):
    aldi = mock_clients[get_aldi_client]
    kroger = mock_clients[get_kroger_client]
    publix = mock_clients[get_publix_client]
    walmart = mock_clients[get_walmart_client]
    aldi.search_products.return_value = [{"retailer": "aldi", "name": "Milk"}]
    kroger.search_products.return_value = [{"retailer": "kroger", "name": "Milk"}]
    publix.search_products.return_value = [{"retailer": "publix", "name": "Milk"}]
    walmart.search_products.return_value = [{"retailer": "walmart", "name": "Milk"}]
    kroger.build_cookies.return_value = {}
    walmart.build_cookies.return_value = {}

    response = client.get("/api/v1/search?q=milk&aldi_location_id=1&kroger_location_id=2")

    assert response.status_code == 200
    assert len(response.json()) == 4
    aldi.search_products.assert_called_once_with("milk", "1", max_results=1)
    kroger.search_products.assert_called_once_with("milk", "2", max_results=1, cookies={})
    publix.search_products.assert_called_once_with("milk", None, max_results=1)
    walmart.search_products.assert_called_once_with("milk", None, max_results=1, cookies=None)
