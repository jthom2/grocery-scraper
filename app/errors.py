class ScraperError(Exception):
    # base class for all scraper-related errors
    def __init__(self, message: str, status_code: int | None = None, url: str | None = None):
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.url = url


class ScraperNetworkError(ScraperError):
    # raised when a network-level error occurs (e.g., timeout, DNS)
    pass


class ScraperBlockedError(ScraperError):
    # raised when the scraper is blocked by anti-bot measures (e.g., 403, 429)
    pass


class ScraperParsingError(ScraperError):
    # raised when the scraper fails to parse the response data (e.g., selector changes)
    pass


class ScraperDataNotFoundError(ScraperError):
    # raised when the requested data (product/store) is not found on the page
    pass
