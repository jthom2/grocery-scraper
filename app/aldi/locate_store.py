import time
import requests

from app.models import normalize_location
from app.utils import fetcher, store_selection
from app.aldi.constants import SEARCH_URL, STORE_FRONT_URL, IDP_SHOPS_URL

#       alt url 'https://info.aldi.us/stores/l/{state_abbrv}/{city}' <- cant get this to work

_COOKIE_CACHE_TTL_SECONDS = 15 * 60
_REQUEST_TIMEOUT_SECONDS = 8
_SESSION = requests.Session()
_COOKIE_CACHE = {
    'cookies': None,
    'expires_at': 0.0,
    'referer': SEARCH_URL,
    'instacart_sid': None,
}


def _prime_instacart_sid(force_refresh=False):
    now = time.time()
    if (
        not force_refresh
        and _COOKIE_CACHE['instacart_sid']
        and _COOKIE_CACHE['expires_at'] > now
    ):
        return _COOKIE_CACHE['instacart_sid']

    warmup = _SESSION.get(
        SEARCH_URL,
        timeout=_REQUEST_TIMEOUT_SECONDS,
        headers={"Referer": SEARCH_URL},
    )
    if warmup.status_code != 200:
        return None

    instacart_sid = _SESSION.cookies.get('__Host-instacart_sid')
    if not instacart_sid:
        return None

    _COOKIE_CACHE['instacart_sid'] = instacart_sid
    _COOKIE_CACHE['expires_at'] = now + _COOKIE_CACHE_TTL_SECONDS
    return instacart_sid


def _prime_store_session(force_refresh=False):
    now = time.time()
    if (
        not force_refresh
        and _COOKIE_CACHE['cookies']
        and _COOKIE_CACHE['expires_at'] > now
    ):
        return _COOKIE_CACHE['cookies'], _COOKIE_CACHE['referer']

    entry = fetcher.fetch(SEARCH_URL)
    referer = SEARCH_URL
    if entry.status != 200:
        entry = fetcher.fetch(STORE_FRONT_URL)
        referer = STORE_FRONT_URL

    if entry.status != 200:
        return None, referer

    _COOKIE_CACHE['cookies'] = entry.cookies
    _COOKIE_CACHE['expires_at'] = now + _COOKIE_CACHE_TTL_SECONDS
    _COOKIE_CACHE['referer'] = referer
    return entry.cookies, referer


def _fetch_shops_direct(zip_code, force_refresh=False):
    instacart_sid = _prime_instacart_sid(force_refresh=force_refresh)
    if not instacart_sid:
        return None

    response = _SESSION.get(
        IDP_SHOPS_URL,
        params={'postal_code': zip_code},
        cookies={'__Host-instacart_sid': instacart_sid},
        headers={"Referer": SEARCH_URL},
        timeout=_REQUEST_TIMEOUT_SECONDS,
    )

    if response.status_code == 401 and not force_refresh:
        return _fetch_shops_direct(zip_code, force_refresh=True)

    if response.status_code != 200:
        return None

    try:
        return response.json().get('shops', [])
    except ValueError:
        return None

def get_stores(zip_code, max_results=10):
    shops_data = _fetch_shops_direct(zip_code)
    if shops_data is None:
        cookies, referer = _prime_store_session()
        if not cookies:
            return []
        page = fetcher.fetch(
            IDP_SHOPS_URL,
            params={'postal_code': zip_code},
            cookies=cookies,
            headers={"Referer": referer},
        )
        if page.status == 401:
            cookies, referer = _prime_store_session(force_refresh=True)
            if not cookies:
                return []
            page = fetcher.fetch(
                IDP_SHOPS_URL,
                params={'postal_code': zip_code},
                cookies=cookies,
                headers={"Referer": referer},
            )
        if page.status != 200:
            return []
        shops_data = page.json().get('shops', [])
    stores = []

    for shop in shops_data[:max_results]:
        _get = shop.get
        address = _get('address', {})
        _get_address = address.get

        street = _get_address('street_address', '')
        city = _get_address('city', '')
        state = _get_address('state', '')
        postal = _get_address('postal_code', '')

        address_line = f"{street}, {city}, {state} {postal}".strip(", ")
        city_state_zip = f"{city}, {state} {postal}".strip(", ")

        stores.append(normalize_location({
            'retailer': 'aldi',
            'name': _get('location_name') or _get('name') or 'ALDI',
            'location_id': str(_get('id')),
            'address': address_line or None,
            'city': city or None,
            'state': state or None,
            'postal_code': postal or None,
            'phone': _get('phone_number'),
            'service_type': _get('fulfillment_option'),
            'metadata': {
                'location_code': _get('location_code'),
                'city_state_zip': city_state_zip,
            },
        }))

    return stores


def display_stores(stores, zip_code):
    print(f"\n{'='*60}")
    print(f"Found {len(stores)} Aldi stores near '{zip_code}'")
    print(f"{'='*60}\n")

    for i, store in enumerate(stores, start=1):
        print(f"{i}. {store['name']}")
        print(f"   {store['address']}")
        if store['phone']:
            print(f"   Phone: {store['phone']}")
        print(f"   Service: {store['service_type']}")
        location_code = store.get('metadata', {}).get('location_code')
        print(f"   Location ID: {store['location_id']} | Location Code: {location_code}\n")


def find_and_select_store():
    zip_code = input("ZIP: ").strip()
    stores = get_stores(zip_code)

    if not stores:
        print("No Aldi stores found.")
        return None, None

    display_stores(stores, zip_code)
    selected = store_selection.select_from_list(stores)

    if selected:
        return selected['location_id'], zip_code

    return None, None


if __name__ == "__main__":
    try:
        zip_code = input("ZIP: ").strip()
        clk = time.time()
        stores = get_stores(zip_code)

        if not stores:
            print("No Aldi stores found.")
        else:
            display_stores(stores, zip_code)
            print(f"\nDone in {time.time() - clk:.2f}s")                # 2.40, 1.99, 2.99, 2.31   avg~2.40
            selected = store_selection.select_from_list(stores)
            if selected:
                print(f"\nSelected: {selected['name']}")
                print(f"Location ID: {selected['location_id']}")
    except:
        pass

