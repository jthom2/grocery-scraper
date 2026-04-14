import pytest
from unittest.mock import MagicMock
from app.utils.fetcher import fetch
from app.utils.get_next_data import get_next_data
from app.errors import ScraperBlockedError, ScraperNetworkError, ScraperParsingError


def test_fetcher_raises_blocked_error():
    mock_page = MagicMock()
    mock_page.status = 403
    mock_page.url = "http://test.com"
    
    with MagicMock() as mock_fetcher:
        mock_fetcher.get.return_value = mock_page
        # Since fetch calls Fetcher.get, we need to mock Fetcher.get
        from app.utils import fetcher
        with pytest.MonkeyPatch().context() as mp:
            mp.setattr(fetcher.Fetcher, "get", lambda *args, **kwargs: mock_page)
            with pytest.raises(ScraperBlockedError) as excinfo:
                fetch("http://test.com")
            assert excinfo.value.status_code == 403


def test_fetcher_raises_network_error():
    mock_page = MagicMock()
    mock_page.status = 500
    mock_page.url = "http://test.com"
    
    from app.utils import fetcher
    with pytest.MonkeyPatch().context() as mp:
        mp.setattr(fetcher.Fetcher, "get", lambda *args, **kwargs: mock_page)
        with pytest.raises(ScraperNetworkError) as excinfo:
            fetch("http://test.com")
        assert excinfo.value.status_code == 500


def test_get_next_data_raises_parsing_error():
    mock_page = MagicMock()
    mock_page.status = 200
    mock_page.url = "http://test.com"
    mock_page.css.return_value = []
    
    with pytest.raises(ScraperParsingError) as excinfo:
        get_next_data(mock_page)
    assert "__NEXT_DATA__ not found" in str(excinfo.value)
