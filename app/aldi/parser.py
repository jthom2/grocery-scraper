import re
from app.models import normalize_product
from app.aldi.constants import BASE_URL

PRICE_PATTERN = re.compile(r"\$([0-9]+(?:\.[0-9]+)?)")


# extracts numeric price value from formatted price string using regex
def parse_price(price_display):
    if not price_display:
        return None

    match = PRICE_PATTERN.search(price_display)
    if not match:
        return None

    return float(match.group(1))


# transforms raw api item data into a standardized product model
def normalize_item(item, location_id):
    _get = item.get
    view_section = _get('viewSection') or {}
    price_view = (_get('price') or {}).get('viewSection', {})
    item_card = price_view.get('itemCard', {})
    item_details = price_view.get('itemDetails', {})
    availability = _get('availability') or {}
    availability_view = availability.get('viewSection', {})
    rating_data = _get('productRating') or {}

    image = (view_section.get('itemImage') or {}).get('url')
    evergreen_url = _get('evergreenUrl')
    price_display = item_card.get('priceString') or item_details.get('priceString')
    
    return normalize_product({
        'retailer': 'aldi',
        'location_id': str(location_id) if location_id else None,
        'product_id': _get('legacyId') or _get('productId'),
        'name': _get('name'),
        'brand': _get('brandName'),
        'size': _get('size'),
        'price': parse_price(price_display),
        'price_display': price_display,
        'unit_price': item_details.get('pricePerUnitString') or item_card.get('pricePerUnitString'),
        'promo_price': None,
        'was_price': item_card.get('fullPriceString') or item_details.get('fullPriceString'),
        'rating': rating_data.get('averageStarRating') or rating_data.get('averageRating'),
        'reviews': rating_data.get('ratingCount') or rating_data.get('numberOfRatings'),
        'image_url': image,
        'in_stock': availability.get('available'),
        'stock_level': availability.get('stockLevel'),
        'availability': availability_view.get('stockLevelLabelString'),
        'url': f"{BASE_URL}/store/aldi/products/{evergreen_url}" if evergreen_url else None,
    })
