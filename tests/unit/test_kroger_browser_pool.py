# verifies browser pool correctly manages session lifecycle
import pytest
from unittest.mock import MagicMock, patch, call
import threading


# singleton pattern prevents multiple browser instances
class TestBrowserPoolSingleton:
    def test_get_instance_returns_same_instance(self):
        from app.kroger.browser_pool import BrowserPool

        BrowserPool._instance = None

        instance1 = BrowserPool.get_instance()
        instance2 = BrowserPool.get_instance()

        assert instance1 is instance2

        BrowserPool._instance = None

    def test_initial_state_not_initialized(self):
        from app.kroger.browser_pool import BrowserPool

        BrowserPool._instance = None

        pool = BrowserPool.get_instance()
        assert pool.is_initialized is False
        assert pool.request_count == 0

        BrowserPool._instance = None

    @patch('app.kroger.browser_pool.StealthySession')
    def test_initialize_creates_session(self, mock_session_class):
        from app.kroger.browser_pool import BrowserPool

        BrowserPool._instance = None

        mock_session = MagicMock()
        mock_session_class.return_value = mock_session

        pool = BrowserPool.get_instance()
        pool._initialize()

        mock_session_class.assert_called_once_with(
            headless=True,
            disable_resources=True,
            network_idle=True,
            timeout=30000,
        )
        mock_session.__enter__.assert_called_once()
        assert pool.is_initialized is True

        BrowserPool._instance = None

    @patch('app.kroger.browser_pool.StealthySession')
    def test_fetch_initializes_on_first_call(self, mock_session_class):
        from app.kroger.browser_pool import BrowserPool

        BrowserPool._instance = None

        mock_session = MagicMock()
        mock_page = MagicMock()
        mock_session.fetch.return_value = mock_page
        mock_session_class.return_value = mock_session

        pool = BrowserPool.get_instance()
        result = pool.fetch('https://example.com')

        assert result is mock_page
        mock_session.fetch.assert_called_once_with('https://example.com', cookies=None)

        BrowserPool._instance = None

    @patch('app.kroger.browser_pool.StealthySession')
    def test_fetch_increments_request_count(self, mock_session_class):
        from app.kroger.browser_pool import BrowserPool

        BrowserPool._instance = None

        mock_session = MagicMock()
        mock_page = MagicMock()
        mock_session.fetch.return_value = mock_page
        mock_session_class.return_value = mock_session

        pool = BrowserPool.get_instance()
        pool.fetch('https://example.com')
        pool.fetch('https://example.com')
        pool.fetch('https://example.com')

        assert pool.request_count == 3

        BrowserPool._instance = None

    @patch('app.kroger.browser_pool.StealthySession')
    def test_cleanup_closes_session(self, mock_session_class):
        from app.kroger.browser_pool import BrowserPool

        BrowserPool._instance = None

        mock_session = MagicMock()
        mock_session_class.return_value = mock_session

        pool = BrowserPool.get_instance()
        pool._initialize()
        pool.cleanup()

        mock_session.__exit__.assert_called_once_with(None, None, None)
        assert pool.is_initialized is False

        BrowserPool._instance = None

    @patch('app.kroger.browser_pool.StealthySession')
    def test_fetch_restarts_on_error(self, mock_session_class):
        from app.kroger.browser_pool import BrowserPool

        BrowserPool._instance = None

        mock_session1 = MagicMock()
        mock_session1.fetch.side_effect = Exception("Browser crashed")

        mock_session2 = MagicMock()
        mock_page = MagicMock()
        mock_session2.fetch.return_value = mock_page

        mock_session_class.side_effect = [mock_session1, mock_session2]

        pool = BrowserPool.get_instance()
        result = pool.fetch('https://example.com')

        assert result is mock_page
        assert mock_session_class.call_count == 2

        BrowserPool._instance = None

    @patch('app.kroger.browser_pool.StealthySession')
    def test_restarts_after_max_requests(self, mock_session_class):
        from app.kroger.browser_pool import BrowserPool

        BrowserPool._instance = None

        mock_session1 = MagicMock()
        mock_page1 = MagicMock()
        mock_session1.fetch.return_value = mock_page1

        mock_session2 = MagicMock()
        mock_page2 = MagicMock()
        mock_session2.fetch.return_value = mock_page2

        mock_session_class.side_effect = [mock_session1, mock_session2]

        pool = BrowserPool.get_instance()
        pool._max_requests_before_restart = 3

        pool.fetch('https://example.com')
        pool.fetch('https://example.com')

        assert mock_session_class.call_count == 1

        pool.fetch('https://example.com')

        assert mock_session_class.call_count == 2

        BrowserPool._instance = None

    @patch('app.kroger.browser_pool.StealthySession')
    def test_passes_cookies_to_session(self, mock_session_class):
        from app.kroger.browser_pool import BrowserPool

        BrowserPool._instance = None

        mock_session = MagicMock()
        mock_page = MagicMock()
        mock_session.fetch.return_value = mock_page
        mock_session_class.return_value = mock_session

        cookies = [{'name': 'test', 'value': 'value', 'url': 'https://example.com'}]

        pool = BrowserPool.get_instance()
        pool.fetch('https://example.com', cookies=cookies)

        mock_session.fetch.assert_called_once_with('https://example.com', cookies=cookies)

        BrowserPool._instance = None


# verifies search function uses pool correctly
class TestKrogerSearchWithPool:
    @patch('app.kroger.search_products.get_browser_pool')
    def test_search_uses_browser_pool(self, mock_get_pool):
        from app.kroger.search_products import search, _USE_BROWSER_POOL

        if not _USE_BROWSER_POOL:
            pytest.skip("Browser pool disabled")

        mock_pool = MagicMock()
        mock_page = MagicMock()
        mock_page.status = 200
        mock_page.css.return_value = []
        mock_pool.fetch.return_value = mock_page
        mock_pool.request_count = 1
        mock_get_pool.return_value = mock_pool

        with pytest.raises(Exception):
            search("test query", max_results=5)

        mock_get_pool.assert_called_once()
        mock_pool.fetch.assert_called_once()

    @patch('app.kroger.search_products.get_browser_pool')
    def test_search_passes_cookies_to_pool(self, mock_get_pool):
        from app.kroger.search_products import search, _USE_BROWSER_POOL

        if not _USE_BROWSER_POOL:
            pytest.skip("Browser pool disabled")

        mock_pool = MagicMock()
        mock_page = MagicMock()
        mock_page.status = 200
        mock_page.css.return_value = []
        mock_pool.fetch.return_value = mock_page
        mock_pool.request_count = 1
        mock_get_pool.return_value = mock_pool

        test_cookies = {'session': 'abc123'}

        with pytest.raises(Exception):
            search("test query", cookies=test_cookies, max_results=5)

        call_args = mock_pool.fetch.call_args
        passed_cookies = call_args[1]['cookies']
        assert passed_cookies is not None
        assert any(c['name'] == 'session' for c in passed_cookies)


# verifies convenience function returns singleton
class TestGetBrowserPool:
    def test_get_browser_pool_returns_singleton(self):
        from app.kroger.browser_pool import get_browser_pool, BrowserPool

        BrowserPool._instance = None

        pool1 = get_browser_pool()
        pool2 = get_browser_pool()

        assert pool1 is pool2

        BrowserPool._instance = None
