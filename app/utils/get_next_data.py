import orjson
from app.errors import ScraperParsingError


def get_next_data(page):
    next_data = page.css('script#__NEXT_DATA__')
    if not next_data:
        raise ScraperParsingError(f"__NEXT_DATA__ not found. Status: {page.status}", status_code=page.status, url=page.url)
    data = orjson.loads(str(next_data[0].text))

    return next_data, data