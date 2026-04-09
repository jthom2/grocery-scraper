import re
import json

from app.utils import fetcher
from app.kroger.constants import REFERER, SEARCH_URL, BASE_URL


class KrogerDataNotFoundError(Exception):
    pass


def extract_initial_state(page):
    scripts = page.css('script')
    for script in scripts:
        text = script.text or ''
        if '__INITIAL_STATE__' in text:
            match = re.search(r"JSON\.parse\('(.+)'\)", text, re.DOTALL)
            if match:
                json_str = match.group(1)
                json_str = json_str.encode('utf-8').decode('unicode_escape')
                return json.loads(json_str)
    raise KrogerDataNotFoundError(f"Status: {page.status} | URL: {page.url}")


def get_front_image(images, size='large'):
    for img in images or []:
        if img.get('perspective') == 'front' and img.get('size') == size:
            return img.get('url')
    return None


def search(query, cookies=None, max_results=5):
    headers = {"Referer": REFERER}
    params = {'query': query, 'searchType': 'default_search'}

    page = fetcher.fetch(SEARCH_URL, params=params, cookies=cookies, headers=headers)

    state = extract_initial_state(page)

    try:
        products_data = state['calypso']['useCases']['getProducts']['search-grid']['response']['data']['products']
    except (KeyError, TypeError):
        return []

    results = []
    for product in products_data[:max_results]:
        item = product.get('item') or {}
        price_data = product.get('price', {}).get('storePrices', {})
        regular = price_data.get('regular', {})
        promo = price_data.get('promo')
        inventory = product.get('inventory', {})
        ratings = item.get('ratingsAndReviewsAggregate', {})

        locations = inventory.get('locations', [])
        stock_level = locations[0].get('stockLevel') if locations else None

        results.append({
            'name': item.get('description'),
            'brand': (item.get('brand') or {}).get('name'),
            'size': item.get('customerFacingSize'),
            'price': regular.get('price'),
            'price_display': regular.get('defaultDescription'),
            'unit_price': regular.get('equivalizedUnitPriceString'),
            'promo_price': promo.get('defaultDescription') if promo else None,
            'rating': ratings.get('averageRating'),
            'reviews': ratings.get('numberOfReviews'),
            'image': get_front_image(item.get('images')),
            'in_stock': stock_level in ('HIGH', 'LOW', 'MEDIUM') if stock_level else None,
            'stock_level': stock_level,
            'upc': product.get('id'),
            'url': f"{BASE_URL}/p/{item.get('seoDescription')}/{product.get('id')}",
        })

    return results


def display_results(results, query):
    print(f"\n{'='*60}")
    print(f"Found {len(results)} products for '{query}'")
    print(f"{'='*60}\n")

    for i, product in enumerate(results, start=1):
        print(f"{i}. {product['name']}")
        if product['brand']:
            print(f"   Brand: {product['brand']}")
        print(f"   Price: {product['price_display'] or product['price'] or 'N/A'}")
        if product['promo_price']:
            print(f"   Sale: {product['promo_price']}")
        if product['unit_price']:
            print(f"   Unit: {product['unit_price']}")
        if product['rating']:
            print(f"   Rating: {product['rating']}/5 ({product['reviews']} reviews)")
        print(f"   In Stock: {product['in_stock']} ({product['stock_level']})")
        print(f"   URL: {product['url']}\n")


if __name__ == "__main__":
    query = input("Search Kroger for: ")
    results = search(query)
    display_results(results, query)
