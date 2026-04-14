import logging

from scrapling.fetchers import Fetcher

logger = logging.getLogger(__name__)


from app.errors import ScraperBlockedError, ScraperNetworkError


def fetch(url, params=None, cookies=None, headers=None):
    page = Fetcher.get(
        url,
        params=params,
        cookies=cookies,
        headers=headers,
        stealthy_headers=True,
        impersonate="chrome",
        timeout=10,
        retries=1,
    )

    if page.status == 403 or page.status == 429:
        raise ScraperBlockedError(f"Blocked by anti-bot: {page.status}", status_code=page.status, url=url)
    elif page.status != 200:
        raise ScraperNetworkError(f"Non-200 response: {page.status}", status_code=page.status, url=url)

    return page

