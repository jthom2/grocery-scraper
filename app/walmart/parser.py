from app.models import normalize_product
from app.walmart.constants import BASE_URL


def normalize_walmart_product(item, location_id=None, cookie_store_id=None):
    _get = item.get
    rating_data = _get('rating') or {}
    price_info = _get('priceInfo') or {}
    availability = _get('availabilityStatusV2') or {}
    image = _get('image')
    
    if isinstance(image, dict):
        image_url = image.get('url')
    else:
        image_url = str(image) if image else None

    return normalize_product({
        'retailer': 'walmart',
        'product_id': _get('usItemId'),
        'location_id': str(location_id) if location_id else cookie_store_id,
        'name': _get('name'),
        'brand': _get('brand'),
        'size': _get('salesUnit'),
        'price': _get('price'),
        'price_display': price_info.get('linePriceDisplay'),
        'unit_price': price_info.get('unitPrice'),
        'was_price': price_info.get('wasPrice') or None,
        'rating': rating_data.get('averageRating'),
        'reviews': rating_data.get('numberOfReviews'),
        'image_url': image_url,
        'in_stock': availability.get('value') == 'IN_STOCK',
        'availability': availability.get('display'),
        'url': f"{BASE_URL}{_get('canonicalUrl', '')}",
        'description': _get('shortDescription', ''),
    })
