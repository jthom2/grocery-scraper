# reuses browser sessions to save ~800-1200ms per request after cold start
import logging
import threading
import atexit

from scrapling.fetchers import StealthySession

logger = logging.getLogger(__name__)


# singleton avoids repeated browser launch overhead, thread-safe
class BrowserPool:
    _instance = None
    _lock = threading.Lock()

    def __init__(self):
        self._session = None
        self._initialized = False
        self._request_count = 0
        self._max_requests_before_restart = 50

    # double-checked locking for thread-safe singleton
    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = cls()
                    atexit.register(cls._instance.cleanup)
        return cls._instance

    # lazy init defers browser launch until first fetch
    def _initialize(self):
        if self._initialized and self._session is not None:
            return

        with self._lock:
            if self._initialized and self._session is not None:
                return

            logger.debug("Initializing Kroger browser pool with StealthySession")
            self._session = StealthySession(
                headless=True,
                disable_resources=True,
                network_idle=True,
                timeout=30000,
            )
            self._session.__enter__()
            self._initialized = True
            self._request_count = 0
            logger.debug("Kroger browser pool initialized")

    # auto-restarts session after max requests to prevent memory leaks
    def fetch(self, url, cookies=None, **kwargs):
        self._initialize()

        self._request_count += 1
        if self._request_count >= self._max_requests_before_restart:
            logger.debug(f"Browser pool reached {self._max_requests_before_restart} requests, restarting")
            self._restart()

        try:
            page = self._session.fetch(url, cookies=cookies, **kwargs)
            return page
        except Exception as e:
            logger.warning(f"Browser pool fetch failed: {e}, restarting session")
            self._restart()
            self._initialize()
            return self._session.fetch(url, cookies=cookies, **kwargs)

    # clears session state without affecting singleton instance
    def _restart(self):
        with self._lock:
            if self._session:
                try:
                    self._session.__exit__(None, None, None)
                except Exception as e:
                    logger.debug(f"Error closing session during restart: {e}")
            self._session = None
            self._initialized = False
            self._request_count = 0

    # atexit registered to prevent orphan browser processes
    def cleanup(self):
        with self._lock:
            if self._session:
                try:
                    self._session.__exit__(None, None, None)
                    logger.debug("Kroger browser pool cleaned up")
                except Exception as e:
                    logger.debug(f"Error during browser pool cleanup: {e}")
            self._session = None
            self._initialized = False
            self._request_count = 0

    # checks both flag and session to handle edge cases during restart
    @property
    def is_initialized(self):
        return self._initialized and self._session is not None

    # tracks requests for auto-restart threshold
    @property
    def request_count(self):
        return self._request_count


_browser_pool = None


# convenience function for imports
def get_browser_pool():
    return BrowserPool.get_instance()
