from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
import pytest

from app.api.main import app

client = TestClient(app)

@patch("app.api.main.aldi_client")
def test_search_aldi(mock_aldi):
    mock_aldi.search_products.return_value = [
        {"retailer": "aldi", "name": "Milk", "price": 2.50}
    ]
    response = client.get("/api/v1/aldi/search?q=milk")
    assert response.status_code == 200
    assert response.json()[0]["name"] == "Milk"
    mock_aldi.search_products.assert_called_with(
        query="milk", location_id=None, max_results=5, zip_code=None
    )

@patch("app.api.main.kroger_client")
def test_search_kroger_with_zip(mock_kroger):
    mock_kroger.get_stores.return_value = [{"location_id": "123"}]
    mock_kroger._build_cookies.return_value = {"k": "v"}
    mock_kroger.search_products.return_value = []
    
    response = client.get("/api/v1/kroger/search?q=bread&zip_code=30303")
    assert response.status_code == 200
    
    mock_kroger.get_stores.assert_called_with("30303")
    mock_kroger._build_cookies.assert_called_with("123", "30303")
    mock_kroger.search_products.assert_called_with(
        query="bread", location_id="123", max_results=5, cookies={"k": "v"}
    )

@patch("app.api.main.publix_client")
def test_search_publix_with_zip(mock_publix):
    mock_publix.get_stores.return_value = [{"location_id": "456"}]
    mock_publix.search_products.return_value = []
    
    response = client.get("/api/v1/publix/search?q=eggs&zip_code=30303")
    assert response.status_code == 200
    
    mock_publix.get_stores.assert_called_with("30303")
    mock_publix.search_products.assert_called_with(
        query="eggs", location_id="456", max_results=5
    )

@patch("app.api.main.walmart_client")
def test_search_walmart_with_zip(mock_walmart):
    mock_walmart.get_stores.return_value = [{"location_id": "789"}]
    mock_walmart._build_cookies.return_value = {"w": "v"}
    mock_walmart.search_products.return_value = []
    
    response = client.get("/api/v1/walmart/search?q=butter&zip_code=30303")
    assert response.status_code == 200
    
    mock_walmart.get_stores.assert_called_with("30303")
    mock_walmart._build_cookies.assert_called_with("789", "30303")
    mock_walmart.search_products.assert_called_with(
        query="butter", location_id="789", max_results=5, cookies={"w": "v"}
    )

@patch("app.api.main.publix_client")
def test_search_publix_error(mock_publix):
    mock_publix.search_products.side_effect = Exception("Scraper error")
    response = client.get("/api/v1/publix/search?q=eggs")
    assert response.status_code == 500
    assert "Scraper error" in response.json()["detail"]
