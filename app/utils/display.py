from typing import Any


def display_products(products: list[dict[str, Any]], query: str, retailer: str) -> None:
    print(f"\n{'='*60}")
    print(f"Found {len(products)} {retailer} products for '{query}'")
    print(f"{'='*60}\n")

    for i, product in enumerate(products, start=1):
        print(f"{i}. {product['name']}")
        if product.get('brand'):
            print(f"   Brand: {product['brand']}")
        if product.get('size'):
            print(f"   Size: {product['size']}")

        price = product.get('price_display') or product.get('price') or 'N/A'
        print(f"   Price: {price}")

        if product.get('promo_price'):
            print(f"   Sale: {product['promo_price']}")
        if product.get('was_price'):
            print(f"   Was: {product['was_price']}")
        if product.get('unit_price'):
            print(f"   Unit: {product['unit_price']}")

        if product.get('rating'):
            reviews = f" ({product['reviews']} reviews)" if product.get('reviews') else ""
            print(f"   Rating: {product['rating']}/5{reviews}")

        stock_info = []
        if product.get('in_stock') is not None:
            stock_info.append(f"In Stock: {product['in_stock']}")
        if product.get('availability'):
            stock_info.append(f"Availability: {product['availability']}")
        if product.get('stock_level'):
            stock_info.append(f"Level: {product['stock_level']}")

        if stock_info:
            print(f"   {' | '.join(stock_info)}")

        if product.get('url'):
            print(f"   URL: {product['url']}")
        print()


def display_stores(stores: list[dict[str, Any]], zip_code: str, retailer: str) -> None:
    print(f"\n{'='*60}")
    print(f"Found {len(stores)} {retailer} stores near '{zip_code}'")
    print(f"{'='*60}\n")

    for i, store in enumerate(stores, start=1):
        print(f"{i}. {store['name']}")
        address_parts = [
            store.get('address'),
            store.get('city'),
            store.get('state'),
            store.get('postal_code'),
        ]
        address = ", ".join(filter(None, address_parts))
        if address:
            print(f"   {address}")

        details = []
        if store.get('phone'):
            details.append(f"Phone: {store['phone']}")
        if store.get('distance'):
            details.append(f"Distance: {store['distance']}")
        if store.get('service_type'):
            details.append(f"Service: {store['service_type']}")

        if details:
            print(f"   {' | '.join(details)}")

        status_parts = []
        if store.get('is_open') is not None:
            status_parts.append("OPEN" if store['is_open'] else "CLOSED")
        if store.get('open_text'):
            status_parts.append(store['open_text'])

        if status_parts:
            print(f"   Status: {' - '.join(status_parts)}")

        print(f"   Location ID: {store['location_id']}")
        print()
