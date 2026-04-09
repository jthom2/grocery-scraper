import logging

from scrapling.fetchers import Fetcher

logger = logging.getLogger(__name__)


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

    if page.status != 200:
        logger.warning(f"Non-200 response: {page.status} | URL: {url}")

    return page

