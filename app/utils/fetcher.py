from scrapling.fetchers import Fetcher

# fetcher template
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
    return page

