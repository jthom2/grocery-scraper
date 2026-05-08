from unittest.mock import MagicMock, patch

import pytest

from app.errors import ScraperBlockedError, ScraperParsingError
from app.kroger.client import KrogerClient


def _state_with_products(count: int):
    return {
        "calypso": {
            "useCases": {
                "getProducts": {
                    "search-grid": {
                        "response": {
                            "data": {
                                "products": [{"id": str(i)} for i in range(count)],
                            }
                        }
                    }
                }
            }
        }
    }


@pytest.fixture(autouse=True)
def _reset_pool_timing_globals(monkeypatch):
    monkeypatch.setattr("app.kroger.client._POOL_WARMUP_DONE", False)
    monkeypatch.setattr("app.kroger.client._POOL_LAST_REQUEST_AT", 0.0)
    monkeypatch.setattr("app.kroger.client._POOL_MIN_INTERVAL_SECONDS", 0.0)
    monkeypatch.setattr("app.kroger.client._POOL_JITTER_SECONDS", 0.0)
    monkeypatch.setattr("app.kroger.client._POOL_BACKOFF_SECONDS", 0.0)


class TestKrogerClientFallback:
    @patch("app.kroger.client.normalize_kroger_product")
    @patch("app.kroger.client.extract_initial_state")
    @patch("app.kroger.client.get_browser_pool")
    @patch("app.kroger.client.StealthyFetcher")
    def test_primary_success_does_not_use_pool(
        self,
        mock_stealthy_fetcher,
        mock_get_pool,
        mock_extract_state,
        mock_normalize,
    ):
        mock_page = MagicMock()
        mock_page.status = 200
        mock_stealthy_fetcher.return_value.fetch.return_value = mock_page
        mock_extract_state.return_value = _state_with_products(2)
        mock_normalize.side_effect = lambda product, location_id=None: {
            "product_id": product["id"],
            "location_id": location_id,
        }

        results = KrogerClient()._fetch_products(
            "milk",
            location_id="014003",
            max_results=1,
            cookies={"session": "abc123"},
        )

        assert results == [{"product_id": "0", "location_id": "014003"}]
        mock_get_pool.assert_not_called()

        fetch_kwargs = mock_stealthy_fetcher.return_value.fetch.call_args.kwargs
        passed_cookies = fetch_kwargs["cookies"]
        assert isinstance(passed_cookies, list)
        assert any(cookie["name"] == "session" and cookie["value"] == "abc123" for cookie in passed_cookies)

    @patch("app.kroger.client.normalize_kroger_product")
    @patch("app.kroger.client.extract_initial_state")
    @patch("app.kroger.client.get_browser_pool")
    @patch("app.kroger.client.StealthyFetcher")
    def test_retries_with_pool_on_403(
        self,
        mock_stealthy_fetcher,
        mock_get_pool,
        mock_extract_state,
        mock_normalize,
    ):
        blocked_page = MagicMock()
        blocked_page.status = 403
        blocked_page.url = "https://www.kroger.com/search?query=milk&searchType=default_search"
        mock_stealthy_fetcher.return_value.fetch.return_value = blocked_page

        pool_page = MagicMock()
        pool_page.status = 200
        mock_pool = MagicMock()
        mock_pool.fetch.return_value = pool_page
        mock_pool.request_count = 1
        mock_get_pool.return_value = mock_pool

        mock_extract_state.return_value = _state_with_products(1)
        mock_normalize.return_value = {"product_id": "0"}

        results = KrogerClient()._fetch_products(
            "milk",
            max_results=1,
            cookies={"session": "abc123"},
        )

        assert results == [{"product_id": "0"}]
        assert mock_pool.fetch.call_count == 2

        pool_kwargs = mock_pool.fetch.call_args_list[-1].kwargs
        passed_cookies = pool_kwargs["cookies"]
        assert isinstance(passed_cookies, list)
        assert any(cookie["name"] == "session" and cookie["value"] == "abc123" for cookie in passed_cookies)

    @patch("app.kroger.client.normalize_kroger_product")
    @patch("app.kroger.client.extract_initial_state")
    @patch("app.kroger.client.get_browser_pool")
    @patch("app.kroger.client.StealthyFetcher")
    def test_retries_with_pool_on_primary_fetch_error(
        self,
        mock_stealthy_fetcher,
        mock_get_pool,
        mock_extract_state,
        mock_normalize,
    ):
        mock_stealthy_fetcher.return_value.fetch.side_effect = RuntimeError("primary fetch crashed")

        pool_page = MagicMock()
        pool_page.status = 200
        mock_pool = MagicMock()
        mock_pool.fetch.return_value = pool_page
        mock_pool.request_count = 1
        mock_get_pool.return_value = mock_pool

        mock_extract_state.return_value = _state_with_products(1)
        mock_normalize.return_value = {"product_id": "0"}

        results = KrogerClient()._fetch_products("milk", max_results=1)

        assert results == [{"product_id": "0"}]
        assert mock_pool.fetch.call_count == 2

    @patch("app.kroger.client._USE_BROWSER_POOL", True)
    @patch("app.kroger.client.normalize_kroger_product")
    @patch("app.kroger.client.extract_initial_state")
    @patch("app.kroger.client.get_browser_pool")
    @patch("app.kroger.client.StealthyFetcher")
    def test_uses_pool_directly_when_enabled(
        self,
        mock_stealthy_fetcher,
        mock_get_pool,
        mock_extract_state,
        mock_normalize,
    ):
        pool_page = MagicMock()
        pool_page.status = 200
        mock_pool = MagicMock()
        mock_pool.fetch.return_value = pool_page
        mock_pool.request_count = 1
        mock_get_pool.return_value = mock_pool

        mock_extract_state.return_value = _state_with_products(1)
        mock_normalize.return_value = {"product_id": "0"}

        results = KrogerClient()._fetch_products("milk", max_results=1, cookies={"session": "abc123"})

        assert results == [{"product_id": "0"}]
        assert mock_pool.fetch.call_count == 2
        mock_stealthy_fetcher.assert_not_called()

    @patch("app.kroger.client.extract_initial_state")
    @patch("app.kroger.client.get_browser_pool")
    @patch("app.kroger.client.StealthyFetcher")
    def test_parser_error_is_raised_without_pool_fallback(
        self,
        mock_stealthy_fetcher,
        mock_get_pool,
        mock_extract_state,
    ):
        ok_page = MagicMock()
        ok_page.status = 200
        mock_stealthy_fetcher.return_value.fetch.return_value = ok_page
        mock_extract_state.side_effect = ScraperParsingError("missing initial state")

        with pytest.raises(ScraperParsingError):
            KrogerClient()._fetch_products("milk", max_results=1)

        mock_get_pool.assert_not_called()

    @patch("app.kroger.client._POOL_MAX_ATTEMPTS", 1)
    @patch("app.kroger.client.logger.warning")
    @patch("app.kroger.client.extract_initial_state")
    @patch("app.kroger.client.get_browser_pool")
    @patch("app.kroger.client.StealthyFetcher")
    def test_logs_block_telemetry_when_blocked(
        self,
        mock_stealthy_fetcher,
        mock_get_pool,
        mock_extract_state,
        mock_warning,
    ):
        blocked_primary = MagicMock()
        blocked_primary.status = 403
        blocked_primary.url = "https://www.kroger.com/search?query=milk&searchType=default_search"
        blocked_primary.headers = {
            "server": "AkamaiGHost",
            "akamai-grn": "0.a4e50b17.1778220410.1069d231",
            "set-cookie": "_abck=test; bm_sz=test;",
        }
        mock_stealthy_fetcher.return_value.fetch.return_value = blocked_primary

        warmup_ok = MagicMock()
        warmup_ok.status = 200
        warmup_ok.url = "https://www.kroger.com/"
        warmup_ok.headers = {}

        blocked_pool = MagicMock()
        blocked_pool.status = 403
        blocked_pool.url = "https://www.kroger.com/search?query=milk&searchType=default_search"
        blocked_pool.headers = {
            "server": "AkamaiGHost",
            "akamai-grn": "0.a4e50b17.1778220410.1069d232",
            "set-cookie": "_abck=test; bm_s=test;",
        }

        mock_pool = MagicMock()
        mock_pool.fetch.side_effect = [warmup_ok, blocked_pool]
        mock_pool.request_count = 1
        mock_get_pool.return_value = mock_pool

        mock_extract_state.side_effect = AssertionError("extract_initial_state should not be called")

        with pytest.raises(ScraperBlockedError):
            KrogerClient()._fetch_products("milk", max_results=1)

        assert mock_warning.call_count >= 2
        telemetry_payload = mock_warning.call_args_list[-1].args[1]
        assert telemetry_payload["fetch_mode"] == "browser_pool"
        assert telemetry_payload["status"] == 403
        assert telemetry_payload["has_abck_cookie"] is True
        assert telemetry_payload["has_bm_cookie"] is True

    @patch("app.kroger.client._USE_BROWSER_POOL", True)
    @patch("app.kroger.client._POOL_MAX_ATTEMPTS", 2)
    @patch("app.kroger.client.normalize_kroger_product")
    @patch("app.kroger.client.extract_initial_state")
    @patch("app.kroger.client.get_browser_pool")
    def test_pool_path_retries_once_before_success(
        self,
        mock_get_pool,
        mock_extract_state,
        mock_normalize,
    ):
        warmup_ok = MagicMock()
        warmup_ok.status = 200
        warmup_ok.url = "https://www.kroger.com/"
        warmup_ok.headers = {}

        blocked_pool = MagicMock()
        blocked_pool.status = 403
        blocked_pool.url = "https://www.kroger.com/search?query=milk&searchType=default_search"
        blocked_pool.headers = {"set-cookie": "_abck=test;"}

        success_pool = MagicMock()
        success_pool.status = 200
        success_pool.url = "https://www.kroger.com/search?query=milk&searchType=default_search"
        success_pool.headers = {}

        mock_pool = MagicMock()
        mock_pool.fetch.side_effect = [warmup_ok, blocked_pool, success_pool]
        mock_pool.request_count = 2
        mock_get_pool.return_value = mock_pool

        mock_extract_state.return_value = _state_with_products(1)
        mock_normalize.return_value = {"product_id": "0"}

        results = KrogerClient()._fetch_products("milk", max_results=1)

        assert results == [{"product_id": "0"}]
        assert mock_pool.fetch.call_count == 3
