from fastapi.testclient import TestClient
from unittest.mock import MagicMock
import pytest

from app.api.main import app
from app.api.dependencies import (
    get_aldi_client, get_kroger_client, get_publix_client, get_walmart_client
)

client = TestClient(app, raise_server_exceptions=False)

@pytest.fixture
def mock_aldi():
    mock = MagicMock()
    app.dependency_overrides[get_aldi_client] = lambda: mock
    yield mock
    app.dependency_overrides.pop(get_aldi_client)

@pytest.fixture
def mock_kroger():
    mock = MagicMock()
    app.dependency_overrides[get_kroger_client] = lambda: mock
    yield mock
    app.dependency_overrides.pop(get_kroger_client)

@pytest.fixture
def mock_publix():
    mock = MagicMock()
    app.dependency_overrides[get_publix_client] = lambda: mock
    yield mock
    app.dependency_overrides.pop(get_publix_client)

@pytest.fixture
def mock_walmart():
    mock = MagicMock()
    app.dependency_overrides[get_walmart_client] = lambda: mock
    yield mock
    app.dependency_overrides.pop(get_walmart_client)


def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_get_aldi_locations(mock_aldi):
    mock_aldi.get_stores.return_value = [{"retailer": "aldi", "location_id": "1", "name": "Store 1"}]
    response = client.get("/api/v1/aldi/locations?zip_code=30303")
    assert response.status_code == 200
    assert response.json()[0]["location_id"] == "1"
    mock_aldi.get_stores.assert_called_once_with("30303", max_results=10)


def test_get_kroger_locations(mock_kroger):
    mock_kroger.get_stores.return_value = []
    response = client.get("/api/v1/kroger/locations?zip_code=90210&max_results=2")
    assert response.status_code == 200
    assert response.json() == []
    mock_kroger.get_stores.assert_called_once_with("90210", max_results=2)


def test_search_aldi(mock_aldi):
    mock_aldi.search_products.return_value = [
        {"retailer": "aldi", "name": "Milk", "price": 2.50}
    ]
    response = client.get("/api/v1/aldi/search?q=milk")
    assert response.status_code == 200
    assert response.json()[0]["name"] == "Milk"
    mock_aldi.search_products.assert_called_once_with(
        query="milk", location_id=None, max_results=5
    )


def test_search_kroger_with_location(mock_kroger):
    mock_kroger._build_cookies.return_value = {"k": "v"}
    mock_kroger.search_products.return_value = []
    
    response = client.get("/api/v1/kroger/search?q=bread&location_id=123")
    assert response.status_code == 200
    
    mock_kroger._build_cookies.assert_called_once_with("123", None)
    mock_kroger.search_products.assert_called_once_with(
        query="bread", location_id="123", max_results=5, cookies={"k": "v"}
    )


def test_search_publix_with_location(mock_publix):
    mock_publix.search_products.return_value = []
    
    response = client.get("/api/v1/publix/search?q=eggs&location_id=456")
    assert response.status_code == 200
    
    mock_publix.search_products.assert_called_once_with(
        query="eggs", location_id="456", max_results=5
    )


def test_search_walmart_with_location(mock_walmart):
    mock_walmart._build_cookies.return_value = {"w": "v"}
    mock_walmart.search_products.return_value = []
    
    response = client.get("/api/v1/walmart/search?q=butter&location_id=789")
    assert response.status_code == 200
    
    mock_walmart._build_cookies.assert_called_once_with("789", None)
    mock_walmart.search_products.assert_called_once_with(
        query="butter", location_id="789", max_results=5, cookies={"w": "v"}
    )


def test_search_publix_error(mock_publix):
    mock_publix.search_products.side_effect = Exception("Scraper error")
    response = client.get("/api/v1/publix/search?q=eggs")
    assert response.status_code == 500
    # verify that the internal error message is NOT leaked
    assert "Scraper error" not in response.json()["detail"]
    assert "internal server error" in response.json()["detail"].lower()


def test_search_all(mock_aldi, mock_kroger, mock_publix, mock_walmart):
    mock_aldi.search_products.return_value = [{"retailer": "aldi", "name": "Milk", "price": 2.50}]
    mock_kroger.search_products.return_value = [{"retailer": "kroger", "name": "Milk", "price": 3.00}]
    mock_publix.search_products.return_value = [{"retailer": "publix", "name": "Milk", "price": 3.50}]
    mock_walmart.search_products.return_value = [{"retailer": "walmart", "name": "Milk", "price": 2.00}]
    
    # ensure kroger/walmart cookie building is mocked if needed (they are called inside unified router)
    mock_kroger._build_cookies.return_value = {}
    mock_walmart._build_cookies.return_value = {}

    response = client.get("/api/v1/search?q=milk&aldi_location_id=1&kroger_location_id=2")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 4
    
    mock_aldi.search_products.assert_called_once_with("milk", "1", max_results=1)
    mock_kroger.search_products.assert_called_once_with("milk", "2", max_results=1, cookies={})
    mock_publix.search_products.assert_called_once_with("milk", None, max_results=1)
    mock_walmart.search_products.assert_called_once_with("milk", None, max_results=1, cookies=None)
