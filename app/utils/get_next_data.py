import orjson


# gathers messy json data
def get_next_data(page):
    
    next_data = page.css('script#__NEXT_DATA__')
    if not next_data:
        print(f"Status: {page.status} | URL: {page.url}")
        exit(1)
    data = orjson.loads(str(next_data[0].text))
    
    return next_data, data

if __name__ == "__main__":
    next_data, data = get_next_data(page)