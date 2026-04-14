"""
Integration tests for locate_store caching across all retailers.
Tests that calling each retailer's locate_store function twice with the same ZIP
uses cache on the second call (should be faster and make fewer network requests).
"""
import time
from unittest.mock import patch, MagicMock

import pytest

from app.walmart import locate_store as walmart_locate
from app.kroger import locate_store as kroger_locate
from app.publix import locate_store as publix_locate
from app.aldi import locate_store as aldi_locate


@pytest.mark.integration
class TestWalmartLocateCaching:
    """Test Walmart locate_store caching with same ZIP twice."""

    @patch('app.walmart.locate_store.zip2loc.get_city_state')
    @patch('app.walmart.locate_store.get_next_data.get_next_data')
    @patch('app.walmart.locate_store.fetcher.fetch')
    def test_walmart_cache_hit_on_second_call(self, mock_fetch, mock_get_next_data, mock_zip2loc):
        """Second call with same ZIP should use cache, not fetch."""
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
        stores1 = walmart_locate.find_stores('98101')
        call_count_after_first = mock_fetch.call_count
        assert len(stores1) > 0, "First call should return stores"

        # Second call with same ZIP
        start = time.time()
        stores2 = walmart_locate.find_stores('98101')
        elapsed = time.time() - start
        call_count_after_second = mock_fetch.call_count

        assert len(stores2) > 0, "Second call should return stores"
        assert call_count_after_second == call_count_after_first, \
            f"Second call should use cache (fetch call count: {call_count_after_first} → {call_count_after_second})"
        print(f"✓ Walmart: Second call used cache ({elapsed*1000:.2f}ms)")


@pytest.mark.integration
class TestKrogerLocateCaching:
    """Test Kroger locate_store caching with same ZIP twice."""

    @patch('app.kroger.locate_store.fetcher.fetch')
    def test_kroger_cache_hit_on_second_call(self, mock_fetch):
        """Second call with same ZIP should use cache."""
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
        stores1 = kroger_locate.get_stores('98101')
        call_count_after_first = mock_fetch.call_count
        assert len(stores1) > 0, "First call should return stores"

        # Second call with same ZIP
        start = time.time()
        stores2 = kroger_locate.get_stores('98101')
        elapsed = time.time() - start
        call_count_after_second = mock_fetch.call_count

        assert len(stores2) > 0, "Second call should return stores"
        assert call_count_after_second == call_count_after_first, \
            f"Second call should use cache (fetch call count: {call_count_after_first} → {call_count_after_second})"
        print(f"✓ Kroger: Second call used cache ({elapsed*1000:.2f}ms)")


@pytest.mark.integration
class TestPublixLocateCaching:
    """Test Publix locate_store caching with same ZIP twice."""

    @patch('app.publix.locate_store.fetcher.fetch')
    def test_publix_cache_hit_on_second_call(self, mock_fetch):
        """Second call with same ZIP should use cache."""
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
        stores1 = publix_locate.fetch_stores('98101')
        call_count_after_first = mock_fetch.call_count
        assert len(stores1) > 0, "First call should return stores"

        # Second call with same ZIP
        start = time.time()
        stores2 = publix_locate.fetch_stores('98101')
        elapsed = time.time() - start
        call_count_after_second = mock_fetch.call_count

        assert len(stores2) > 0, "Second call should return stores"
        assert call_count_after_second == call_count_after_first, \
            f"Second call should use cache (fetch call count: {call_count_after_first} → {call_count_after_second})"
        print(f"✓ Publix: Second call used cache ({elapsed*1000:.2f}ms)")


@pytest.mark.integration
class TestAldiLocateCaching:
    """Test Aldi locate_store caching with same ZIP twice."""

    @patch('app.aldi.locate_store._fetch_shops_direct')
    @patch('app.aldi.locate_store._prime_session')
    def test_aldi_cache_hit_on_second_call(self, mock_prime_session, mock_fetch_shops):
        """Second call with same ZIP should use cache."""
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
        stores1 = aldi_locate.get_stores('98101')
        fetch_call_count_after_first = mock_fetch_shops.call_count
        assert len(stores1) > 0, "First call should return stores"

        # Second call with same ZIP
        start = time.time()
        stores2 = aldi_locate.get_stores('98101')
        elapsed = time.time() - start
        fetch_call_count_after_second = mock_fetch_shops.call_count

        assert len(stores2) > 0, "Second call should return stores"
        assert fetch_call_count_after_second == fetch_call_count_after_first, \
            f"Second call should use cache (_fetch_shops_direct call count: {fetch_call_count_after_first} → {fetch_call_count_after_second})"
        print(f"✓ Aldi: Second call used cache ({elapsed*1000:.2f}ms)")
