from scrapling.fetchers import Fetcher

def fetch(url, params=None):
    if params is None:
        page = Fetcher.get(
            url,
            stealthy_headers=True,
            impersonate="chrome",
            timeout=10,
            retries=1,
        )
        return page
    else:
        page = Fetcher.get(
            'https://www.walmart.com/search',
            params=params,
            stealthy_headers=True,
            impersonate="chrome",
            timeout=10,
            retries=1,
        )
        return page

if __name__ == "__main__":
    fetcher(url, params)
