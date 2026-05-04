from urllib.parse import quote

from app.models import normalize_location, normalize_product
from app.utils import zip2loc, get_next_data, fetcher
from app.utils.store_client import BaseStoreClient
from app.walmart import build_cookies
from app.walmart.constants import STORE_DIRECTORY_URL, REFERER, SEARCH_URL, BASE_URL
from app.walmart.parser import normalize_walmart_product


class WalmartClient(BaseStoreClient):

    @property
    def retailer_name(self) -> str:
        return "walmart"

    def build_cookies(self, location_id, zip_code):
        return build_cookies.build_location_cookies(location_id, zip_code)

    # converts zip code to city/state and fetches nearby walmart store locations
    def _fetch_stores(self, zip_code, max_results=4):
        city, state = zip2loc.get_city_state(zip_code)

        if not city or not state:
            print(f"Error: Could not find location for zip code '{zip_code}'.")
            return []

        url = f'{STORE_DIRECTORY_URL}/{quote(state, safe="")}/{quote(city, safe="")}'
        page = fetcher.fetch(url)

        next_data, data = get_next_data.get_next_data(page)

        nearby_nodes = (
            data.get('props', {})
            .get('pageProps', {})
            .get('initialData', {})
            .get('initialDataNearbyNodes', {})
            .get('data', {})
            .get('nearByNodes', {})
            .get('nodes', [])
        )

        if not nearby_nodes:
            return []

        stores = []
        for node in nearby_nodes[:max_results]:
            name = node.get('displayName') or node.get('name') or "Unknown Store"

            address_info = node.get('address', {})
            addr_line_1 = address_info.get('addressLineOne', '')
            addr_city = address_info.get('city', '')
            addr_state = address_info.get('state', '')
            addr_zip = address_info.get('postalCode', '')

            address_str = f"{addr_line_1}, {addr_city}, {addr_state} {addr_zip}".strip(", ")
            store_id = str(node.get('id', 'N/A'))

            stores.append(normalize_location({
                'retailer': 'walmart',
                'location_id': store_id,
                'name': name,
                'address': address_str or None,
                'city': addr_city or None,
                'state': addr_state or None,
                'postal_code': addr_zip or None,
                'metadata': {
                    'address_info': address_info,
                },
            }))

        return stores

    # fetches and normalizes walmart product search results with optional store filtering
    def _fetch_products(self, query, location_id=None, max_results=5, **kwargs):
        cookies = kwargs.get('cookies')

        # resolve store_id for cache key consistency
        cookie_store_id = str(cookies.get('assortmentStoreId')) if cookies and cookies.get('assortmentStoreId') else None
        store_id = str(location_id) if location_id else cookie_store_id

        headers = {"Referer": REFERER}

        page = fetcher.fetch(SEARCH_URL, params={'q': query}, cookies=cookies, headers=headers)

        next_data, data = get_next_data.get_next_data(page)

        item_stacks = data['props']['pageProps']['initialData']['searchResult']['itemStacks']

        results = []
        result_count = 0

        for stack in item_stacks:
            if result_count >= max_results:
                break
            for item in stack.get('items', ()):
                if result_count >= max_results:
                    break

                if not (name := item.get('name')) or item.get('__typename') == 'SearchPlaceholderProduct':
                    continue

                if cookies and (cookie_sid := cookies.get('assortmentStoreId')):
                    fulfillment_opts = item.get('fulfillmentSummary') or []
                    is_in_store = any(str(f.get('storeId')) == str(cookie_sid) for f in fulfillment_opts)
                    if not is_in_store:
                        continue

                results.append(normalize_walmart_product(item, location_id, cookie_store_id))
                result_count += 1

        return results


def main():
    from app.cli import run_interactive_search
    run_interactive_search(WalmartClient())


if __name__ == "__main__":
    main()
