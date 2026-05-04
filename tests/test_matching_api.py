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

    response = client.post("/api/v1/match/search", json={
        "query": "2% milk 1 gallon",
        "retailers": ["walmart", "kroger"],
        "location_ids": {"walmart": "789", "kroger": "123"},
        "zip_code": "30303",
        "max_candidates_per_retailer": 3,
    })

    assert response.status_code == 200
    data = response.json()
    assert len(data["equivalent"]) == 2
    assert data["errors"] == {}
    walmart.search_products.assert_called_once_with(
        query="2% milk 1 gallon",
        location_id="789",
        max_results=3,
        cookies={"w": "v"},
    )
    kroger.search_products.assert_called_once_with(
        query="2% milk 1 gallon",
        location_id="123",
        max_results=3,
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
    assert data["errors"] == {"walmart": "blocked"}
    assert len(data["equivalent"]) == 1


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
