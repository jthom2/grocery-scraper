"""Unit tests for ZIP code to location lookup."""
import pytest

from app.utils.zip2loc import get_city_state


class TestGetCityState:
    """Test ZIP to city/state conversion."""

    def test_valid_zip_returns_city_state(self, mock_requests_get):
        """Valid ZIP returns (city, state) tuple."""
        mock_requests_get.return_value.status_code = 200
        mock_requests_get.return_value.json.return_value = {
            "places": [{"place name": "Beverly Hills", "state abbreviation": "CA"}]
        }

        city, state = get_city_state("90210")

        assert city == "Beverly Hills"
        assert state == "CA"
        mock_requests_get.assert_called_once()

    def test_invalid_zip_returns_none_tuple(self, mock_requests_get):
        """Invalid ZIP returns (None, None)."""
        mock_requests_get.return_value.status_code = 404

        city, state = get_city_state("00000")

        assert city is None
        assert state is None

    def test_no_places_returns_none_tuple(self, mock_requests_get):
        """Empty places array returns (None, None)."""
        mock_requests_get.return_value.status_code = 200
        mock_requests_get.return_value.json.return_value = {"places": []}

        city, state = get_city_state("99999")

        assert city is None
        assert state is None

    def test_missing_places_key_returns_none_tuple(self, mock_requests_get):
        """Missing 'places' key returns (None, None)."""
        mock_requests_get.return_value.status_code = 200
        mock_requests_get.return_value.json.return_value = {}

        city, state = get_city_state("12345")

        assert city is None
        assert state is None

    def test_calls_correct_api_url(self, mock_requests_get):
        """API is called with correct URL."""
        mock_requests_get.return_value.status_code = 200
        mock_requests_get.return_value.json.return_value = {
            "places": [{"place name": "Test City", "state abbreviation": "TX"}]
        }

        get_city_state("75001")

        call_args = mock_requests_get.call_args
        assert "75001" in call_args[0][0]
        assert "zippopotam.us" in call_args[0][0]

    def test_timeout_is_set(self, mock_requests_get):
        """Request includes timeout parameter."""
        mock_requests_get.return_value.status_code = 200
        mock_requests_get.return_value.json.return_value = {
            "places": [{"place name": "Test", "state abbreviation": "CA"}]
        }

        get_city_state("90210")

        call_kwargs = mock_requests_get.call_args[1]
        assert call_kwargs.get("timeout") == 10
