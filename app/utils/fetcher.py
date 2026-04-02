from scrapling.fetchers import Fetcher

# fetcher template
def fetch(url, params=None):
    page = Fetcher.get(
        url,
        params=params,
        stealthy_headers=True,
        impersonate="chrome",
        timeout=10,
        retries=1,
    )
    return page
