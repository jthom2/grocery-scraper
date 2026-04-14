# validates zip lookup handles api responses correctly with new Scraper errors
import pytest
from app.utils.zip2loc import get_city_state, _fetch_from_api
from app.errors import ScraperDataNotFoundError, ScraperNetworkError, ScraperParsingError


class TestGetCityState:
    # happy path: api returns valid location data
    def test_valid_zip_returns_city_state(self, mock_requests_get):
        mock_requests_get.return_value.status_code = 200
        mock_requests_get.return_value.json.return_value = {
            "places": [{"place name": "Beverly Hills", "state abbreviation": "CA"}]
        }

        # Clear cache to avoid side effects between tests
        _fetch_from_api.cache_clear()
        city, state = get_city_state("90210")

        assert city == "Beverly Hills"
        assert state == "CA"
        mock_requests_get.assert_called_once()

    # 404 should raise ScraperDataNotFoundError
    def test_invalid_zip_raises_data_not_found(self, mock_requests_get):
        mock_requests_get.return_value.status_code = 404
        _fetch_from_api.cache_clear()

        with pytest.raises(ScraperDataNotFoundError) as excinfo:
            get_city_state("00000")
        
        assert "ZIP code not found" in str(excinfo.value)
        assert excinfo.value.status_code == 404

    # 500 should raise ScraperNetworkError
    def test_server_error_raises_network_error(self, mock_requests_get):
        mock_requests_get.return_value.status_code = 500
        _fetch_from_api.cache_clear()

        with pytest.raises(ScraperNetworkError) as excinfo:
            get_city_state("55555")
        
        assert "API returned 500" in str(excinfo.value)

    # edge case: api returns empty places list
    def test_no_places_raises_parsing_error(self, mock_requests_get):
        mock_requests_get.return_value.status_code = 200
        mock_requests_get.return_value.json.return_value = {"places": []}
        _fetch_from_api.cache_clear()

        with pytest.raises(ScraperParsingError) as excinfo:
            get_city_state("99999")
        
        assert "Unexpected API response" in str(excinfo.value)

    # ensures we hit the right endpoint format
    def test_calls_correct_api_url(self, mock_requests_get):
        mock_requests_get.return_value.status_code = 200
        mock_requests_get.return_value.json.return_value = {
            "places": [{"place name": "Test City", "state abbreviation": "TX"}]
        }
        _fetch_from_api.cache_clear()

        get_city_state("75001")

        call_args = mock_requests_get.call_args
        assert "75001" in call_args[0][0]
        assert "zippopotam.us" in call_args[0][0]
