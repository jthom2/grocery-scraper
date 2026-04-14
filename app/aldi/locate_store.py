import time
import requests

from app.models import normalize_location
from app.utils import fetcher, store_selection, display
from app.utils.cache import TTLCache
from app.utils.store_cache import store_cache
from app.aldi.constants import SEARCH_URL, STORE_FRONT_URL, IDP_SHOPS_URL

_SESSION_CACHE = TTLCache(ttl_seconds=15 * 60)
_REQUEST_TIMEOUT = 8
_SESSION = requests.Session()


from app.errors import ScraperNetworkError, ScraperBlockedError, ScraperParsingError


def _prime_session(force_refresh=False):
    cached = _SESSION_CACHE.get('session')
    if cached and not force_refresh:
        return cached

    # attempt to get instacart_sid first via requests (faster)
    try:
        warmup = _SESSION.get(SEARCH_URL, timeout=_REQUEST_TIMEOUT, headers={"Referer": SEARCH_URL})
        instacart_sid = _SESSION.cookies.get('__Host-instacart_sid')
    except requests.RequestException:
        instacart_sid = None

    # also get full cookies/referer via fetcher for fallback path
    entry = fetcher.fetch(SEARCH_URL)
    referer = SEARCH_URL
    if entry.status != 200:
        entry = fetcher.fetch(STORE_FRONT_URL)
        referer = STORE_FRONT_URL

    if entry.status == 403 or entry.status == 429:
        raise ScraperBlockedError(f"Blocked by anti-bot: {entry.status}", status_code=entry.status, url=entry.url)
    elif entry.status != 200:
        raise ScraperNetworkError(f"Failed to prime session. Status: {entry.status}", status_code=entry.status, url=entry.url)

    session_data = {
        'cookies': entry.cookies,
        'referer': referer,
        'instacart_sid': instacart_sid
    }
    _SESSION_CACHE.set('session', session_data)
    return session_data


def _fetch_shops_direct(zip_code, force_refresh=False):
    session = _prime_session(force_refresh=force_refresh)
    if not session['instacart_sid']:
        return None

    try:
        response = _SESSION.get(
            IDP_SHOPS_URL,
            params={'postal_code': zip_code},
            cookies={'__Host-instacart_sid': session['instacart_sid']},
            headers={"Referer": SEARCH_URL},
            timeout=_REQUEST_TIMEOUT,
        )
    except requests.RequestException as e:
        raise ScraperNetworkError(f"Direct shop fetch failed: {e}", url=IDP_SHOPS_URL)

    if response.status_code == 401 and not force_refresh:
        return _fetch_shops_direct(zip_code, force_refresh=True)

    if response.status_code == 403 or response.status_code == 429:
        raise ScraperBlockedError(f"Blocked by anti-bot: {response.status_code}", status_code=response.status_code, url=IDP_SHOPS_URL)

    try:
        return response.json().get('shops', []) if response.status_code == 200 else None
    except (ValueError, AttributeError):
        raise ScraperParsingError(f"Failed to parse direct shop response", status_code=response.status_code, url=IDP_SHOPS_URL)


def get_stores(zip_code, max_results=10):
    # attempt to retrieve from cache (Cache-Aside: Read)
    if cached_stores := store_cache.get('aldi', zip_code):
        return cached_stores[:max_results]

    shops_data = _fetch_shops_direct(zip_code)
    
    # fallback to fetcher if direct requests failed
    if shops_data is None:
        session = _prime_session()
        if not session['cookies']:
            return []
            
        page = fetcher.fetch(
            IDP_SHOPS_URL,
            params={'postal_code': zip_code},
            cookies=session['cookies'],
            headers={"Referer": session['referer']},
        )
        if page.status == 401:
            session = _prime_session(force_refresh=True)
            page = fetcher.fetch(
                IDP_SHOPS_URL,
                params={'postal_code': zip_code},
                cookies=session['cookies'],
                headers={"Referer": session['referer']},
            )
        shops_data = page.json().get('shops', []) if page.status == 200 else []

    stores = []
    for shop in (shops_data or [])[:max_results]:
        addr = shop.get('address', {})
        street, city, state, postal = addr.get('street_address', ''), addr.get('city', ''), addr.get('state', ''), addr.get('postal_code', '')
        
        stores.append(normalize_location({
            'retailer': 'aldi',
            'name': shop.get('location_name') or shop.get('name') or 'ALDI',
            'location_id': str(shop.get('id')),
            'address': f"{street}, {city}, {state} {postal}".strip(", ") or None,
            'city': city or None,
            'state': state or None,
            'postal_code': postal or None,
            'phone': shop.get('phone_number'),
            'service_type': shop.get('fulfillment_option'),
            'metadata': {
                'location_code': shop.get('location_code'),
                'city_state_zip': f"{city}, {state} {postal}".strip(", "),
            },
        }))
    
    # store in cache for 24 hours (Cache-Aside: Write)
    if stores:
        store_cache.set('aldi', zip_code, stores)

    return stores


def display_stores(stores, zip_code):
    display.display_stores(stores, zip_code, "Aldi")


def find_and_select_store():
    zip_code = input("ZIP: ").strip()
    stores = get_stores(zip_code)

    if not stores:
        print("No Aldi stores found.")
        return None, None

    display_stores(stores, zip_code)
    selected = store_selection.select_from_list(stores)
    return (selected['location_id'], zip_code) if selected else (None, None)


if __name__ == "__main__":
    zip_in = input("ZIP: ").strip()
    start = time.time()
    results = get_stores(zip_in)
    if results:
        display_stores(results, zip_in)
        print(f"\nDone in {time.time() - start:.2f}s")
        sel = store_selection.select_from_list(results)
        if sel:
            print(f"\nSelected: {sel['name']}\nLocation ID: {sel['location_id']}")
    else:
        print("No stores found.")
