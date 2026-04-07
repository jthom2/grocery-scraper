import orjson


class NextDataNotFoundError(Exception):
    pass


def get_next_data(page):
    next_data = page.css('script#__NEXT_DATA__')
    if not next_data:
        raise NextDataNotFoundError(f"Status: {page.status} | URL: {page.url}")
    data = orjson.loads(str(next_data[0].text))

    return next_data, data