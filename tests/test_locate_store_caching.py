import unittest.mock
# integration tests for locate_store caching across all retailers
# tests that calling each retailer's locate_store function twice with the same ZIP
# uses cache on the second call (should be faster and make fewer network requests)
import time
from unittest.mock import patch, MagicMock

import pytest

from app.walmart.client import WalmartClient
from app.kroger.client import KrogerClient
from app.publix.client import PublixClient
from app.aldi.client import AldiClient


@pytest.mark.integration
class TestWalmartLocateCaching:
    # test Walmart locate_store caching with same ZIP twice

    def setup_method(self):
        from app.utils.store_cache import store_cache
        store_cache._client = MagicMock()
        self.cache_data = {}
        def mock_get(k, default=None): return self.cache_data.get(k)
        def mock_set(k, v, *args, **kwargs): self.cache_data[k] = v
        store_cache._client.get = mock_get
        store_cache._client.setex = mock_set

        # Actually it's probably using Redis, so we can just mock store_cache methods
        store_cache.get = lambda retailer, zip_code: self.cache_data.get(f"{retailer}:{zip_code}")
        store_cache.set = lambda retailer, zip_code, stores, ttl_hours=1: self.cache_data.update({f"{retailer}:{zip_code}": stores})


    @patch('app.walmart.client.zip2loc.get_city_state')
    @patch('app.walmart.client.get_next_data.get_next_data')
    @patch('app.walmart.client.fetcher.fetch')
    def test_walmart_cache_hit_on_second_call(self, mock_fetch, mock_get_next_data, mock_zip2loc):
        # second call with same ZIP should use cache, not fetch
        mock_zip2loc.return_value = ('Seattle', 'WA')

        # Mock the page object with css() and text attributes
        mock_script = MagicMock()
        mock_script.text = '{"props":{"pageProps":{"initialData":{"initialDataNearbyNodes":{"data":{"nearByNodes":{"nodes":[{"id":1,"displayName":"Walmart Seattle","address":{"addressLineOne":"123 Main","city":"Seattle","state":"WA","postalCode":"98101"}}]}}}}}}}'
        mock_get_next_data.return_value = ([mock_script], {
            'props': {
                'pageProps': {
                    'initialData': {
                        'initialDataNearbyNodes': {
                            'data': {
                                'nearByNodes': {
                                    'nodes': [{
                                        'id': 1,
                                        'displayName': 'Walmart Seattle',
                                        'address': {
                                            'addressLineOne': '123 Main',
                                            'city': 'Seattle',
                                            'state': 'WA',
                                            'postalCode': '98101'
                                        }
                                    }]
                                }
                            }
                        }
                    }
                }
            }
        })

        mock_fetch.return_value = MagicMock()

        # First call
        stores1 = WalmartClient().get_stores('98101')
        call_count_after_first = mock_fetch.call_count
        assert len(stores1) > 0, "First call should return stores"

        # Second call with same ZIP
        start = time.time()
        stores2 = WalmartClient().get_stores('98101')
        elapsed = time.time() - start
        call_count_after_second = mock_fetch.call_count

        assert len(stores2) > 0, "Second call should return stores"
        assert call_count_after_second == call_count_after_first, \
            f"Second call should use cache (fetch call count: {call_count_after_first} → {call_count_after_second})"
        print(f"✓ Walmart: Second call used cache ({elapsed*1000:.2f}ms)")


@pytest.mark.integration
class TestKrogerLocateCaching:
    # test Kroger locate_store caching with same ZIP twice

    def setup_method(self):
        from app.utils.store_cache import store_cache
        store_cache._client = MagicMock()
        self.cache_data = {}
        def mock_get(k, default=None): return self.cache_data.get(k)
        def mock_set(k, v, *args, **kwargs): self.cache_data[k] = v
        store_cache._client.get = mock_get
        store_cache._client.setex = mock_set

        # Actually it's probably using Redis, so we can just mock store_cache methods
        store_cache.get = lambda retailer, zip_code: self.cache_data.get(f"{retailer}:{zip_code}")
        store_cache.set = lambda retailer, zip_code, stores, ttl_hours=1: self.cache_data.update({f"{retailer}:{zip_code}": stores})


    @patch('app.kroger.client.fetcher.fetch')
    def test_kroger_cache_hit_on_second_call(self, mock_fetch):
        # second call with same ZIP should use cache
        mock_response = MagicMock()
        mock_response.status = 200
        mock_response.json.return_value = {
            'data': {
                'stores': [{
                    'locationId': 1,
                    'vanityName': 'Kroger Seattle',
                    'banner': 'KROGER',
                    'locale': {
                        'address': {
                            'addressLines': ['123 Main St'],
                            'cityTown': 'Seattle',
                            'stateProvince': 'WA',
                            'postalCode': '98101'
                        },
                        'location': {'latitude': 47.6, 'longitude': -122.3}
                    },
                    'phoneNumber': {'pretty': '206-555-0100'},
                    'distance': {'pretty': '2 mi'}
                }]
            }
        }
        mock_fetch.return_value = mock_response

        # First call
        stores1 = KrogerClient().get_stores('98101')
        call_count_after_first = mock_fetch.call_count
        assert len(stores1) > 0, "First call should return stores"

        # Second call with same ZIP
        start = time.time()
        stores2 = KrogerClient().get_stores('98101')
        elapsed = time.time() - start
        call_count_after_second = mock_fetch.call_count

        assert len(stores2) > 0, "Second call should return stores"
        assert call_count_after_second == call_count_after_first, \
            f"Second call should use cache (fetch call count: {call_count_after_first} → {call_count_after_second})"
        print(f"✓ Kroger: Second call used cache ({elapsed*1000:.2f}ms)")


@pytest.mark.integration
class TestPublixLocateCaching:
    # test Publix locate_store caching with same ZIP twice

    def setup_method(self):
        from app.utils.store_cache import store_cache
        store_cache._client = MagicMock()
        self.cache_data = {}
        def mock_get(k, default=None): return self.cache_data.get(k)
        def mock_set(k, v, *args, **kwargs): self.cache_data[k] = v
        store_cache._client.get = mock_get
        store_cache._client.setex = mock_set

        # Actually it's probably using Redis, so we can just mock store_cache methods
        store_cache.get = lambda retailer, zip_code: self.cache_data.get(f"{retailer}:{zip_code}")
        store_cache.set = lambda retailer, zip_code, stores, ttl_hours=1: self.cache_data.update({f"{retailer}:{zip_code}": stores})


    @patch('app.publix.client.fetcher.fetch')
    def test_publix_cache_hit_on_second_call(self, mock_fetch):
        # second call with same ZIP should use cache
        mock_response = MagicMock()
        mock_response.json.return_value = {
            'stores': [{
                'storeNumber': 1,
                'name': 'Publix Seattle',
                'shortName': 'Publix',
                'address': {
                    'streetAddress': '123 Main St',
                    'city': 'Seattle',
                    'state': 'WA',
                    'zip': '98101'
                },
                'phoneNumbers': {'Store': '206-555-0100'}
            }]
        }
        mock_fetch.return_value = mock_response

        # First call
        stores1 = PublixClient().get_stores('98101')
        call_count_after_first = mock_fetch.call_count
        assert len(stores1) > 0, "First call should return stores"

        # Second call with same ZIP
        start = time.time()
        stores2 = PublixClient().get_stores('98101')
        elapsed = time.time() - start
        call_count_after_second = mock_fetch.call_count

        assert len(stores2) > 0, "Second call should return stores"
        assert call_count_after_second == call_count_after_first, \
            f"Second call should use cache (fetch call count: {call_count_after_first} → {call_count_after_second})"
        print(f"✓ Publix: Second call used cache ({elapsed*1000:.2f}ms)")


@pytest.mark.integration
class TestAldiLocateCaching:
    # test Aldi locate_store caching with same ZIP twice

    def setup_method(self):
        from app.utils.store_cache import store_cache
        store_cache._client = MagicMock()
        self.cache_data = {}
        def mock_get(k, default=None): return self.cache_data.get(k)
        def mock_set(k, v, *args, **kwargs): self.cache_data[k] = v
        store_cache._client.get = mock_get
        store_cache._client.setex = mock_set

        # Actually it's probably using Redis, so we can just mock store_cache methods
        store_cache.get = lambda retailer, zip_code: self.cache_data.get(f"{retailer}:{zip_code}")
        store_cache.set = lambda retailer, zip_code, stores, ttl_hours=1: self.cache_data.update({f"{retailer}:{zip_code}": stores})


    @patch('app.aldi.client._fetch_shops_direct')
    @patch('app.aldi.client._prime_session')
    def test_aldi_cache_hit_on_second_call(self, mock_prime_session, mock_fetch_shops):
        # second call with same ZIP should use cache
        # Mock the shops response from direct fetch
        mock_fetch_shops.return_value = [{
            'id': '1',
            'location_name': 'ALDI Seattle',
            'address': {
                'street_address': '123 Main St',
                'city': 'Seattle',
                'state': 'WA',
                'postal_code': '98101'
            }
        }]

        # First call
        stores1 = AldiClient().get_stores('98101')
        fetch_call_count_after_first = mock_fetch_shops.call_count
        assert len(stores1) > 0, "First call should return stores"

        # Second call with same ZIP
        start = time.time()
        stores2 = AldiClient().get_stores('98101')
        elapsed = time.time() - start
        fetch_call_count_after_second = mock_fetch_shops.call_count

        assert len(stores2) > 0, "Second call should return stores"
        assert fetch_call_count_after_second == fetch_call_count_after_first, \
            f"Second call should use cache (_fetch_shops_direct call count: {fetch_call_count_after_first} → {fetch_call_count_after_second})"
        print(f"✓ Aldi: Second call used cache ({elapsed*1000:.2f}ms)")
