# verifies fetcher-first strategy reduces stealthyfetcher usage
import pytest
from unittest.mock import MagicMock, patch

from app.publix.search_products import search, _has_product_content


# validates content detection to decide fast vs slow path
class TestHasProductContent:
    def test_returns_true_for_product_aria_label(self):
        html = '<a aria-label="$9.99 - Test Product">Product</a>'
        assert _has_product_content(html) is True

    def test_returns_true_for_price_with_decimals(self):
        html = '<a aria-label="$12.34 - Item Name">Link</a>'
        assert _has_product_content(html) is True

    def test_returns_false_for_no_price(self):
        html = '<a aria-label="Test Product">Product</a>'
        assert _has_product_content(html) is False

    def test_returns_false_for_empty_html(self):
        assert _has_product_content('') is False

    def test_returns_false_for_no_aria_labels(self):
        html = '<div>No products here</div>'
        assert _has_product_content(html) is False


# ensures fallback logic triggers correctly
class TestPublixFetcherFirstStrategy:
    @patch('app.publix.search_products.StealthyFetcher')
    @patch('app.publix.search_products.Fetcher')
    def test_uses_fast_path_when_fetcher_succeeds(self, mock_fetcher, mock_stealthy):
        mock_page = MagicMock()
        mock_page.status = 200
        mock_page.body = '''
            <html>
            <body>
                <a href="/pd/test-product/RIO-PCI-123" aria-label="$9.99 - Test Product">Link</a>
            </body>
            </html>
        '''
        mock_fetcher.get.return_value = mock_page

        results = search("milk", max_results=5)

        mock_fetcher.get.assert_called_once()
        mock_stealthy.assert_not_called()

    @patch('app.publix.search_products.StealthyFetcher')
    @patch('app.publix.search_products.Fetcher')
    def test_falls_back_to_stealthy_on_fetcher_failure(self, mock_fetcher, mock_stealthy):
        mock_fetcher.get.side_effect = Exception("Connection failed")

        mock_redirect_page = MagicMock()
        mock_redirect_page.status = 200
        mock_redirect_page.headers = {}

        mock_fetcher.get.side_effect = [
            Exception("Connection failed"),
            mock_redirect_page,
        ]

        mock_stealthy_instance = MagicMock()
        mock_stealthy_page = MagicMock()
        mock_stealthy_page.status = 200
        mock_stealthy_page.body = '<html><body></body></html>'
        mock_stealthy_instance.fetch.return_value = mock_stealthy_page
        mock_stealthy.return_value = mock_stealthy_instance

        results = search("milk", max_results=5)

        mock_stealthy.assert_called_once()
        mock_stealthy_instance.fetch.assert_called_once()

    @patch('app.publix.search_products.StealthyFetcher')
    @patch('app.publix.search_products.Fetcher')
    def test_falls_back_when_content_validation_fails(self, mock_fetcher, mock_stealthy):
        mock_page = MagicMock()
        mock_page.status = 200
        mock_page.body = '<html><body>No products here</body></html>'

        mock_redirect_page = MagicMock()
        mock_redirect_page.status = 200
        mock_redirect_page.headers = {}

        mock_fetcher.get.side_effect = [mock_page, mock_redirect_page]

        mock_stealthy_instance = MagicMock()
        mock_stealthy_page = MagicMock()
        mock_stealthy_page.status = 200
        mock_stealthy_page.body = '<html><body></body></html>'
        mock_stealthy_instance.fetch.return_value = mock_stealthy_page
        mock_stealthy.return_value = mock_stealthy_instance

        results = search("milk", max_results=5)

        assert mock_fetcher.get.call_count == 2
        mock_stealthy.assert_called_once()

    @patch('app.publix.search_products.StealthyFetcher')
    @patch('app.publix.search_products.Fetcher')
    def test_falls_back_when_store_context_missing(self, mock_fetcher, mock_stealthy):
        mock_page = MagicMock()
        mock_page.status = 200
        mock_page.body = '''
            <html>
            <body>
                <a href="/pd/test-product/RIO-PCI-123" aria-label="$9.99 - Test Product">Link</a>
            </body>
            </html>
        '''

        mock_redirect_page = MagicMock()
        mock_redirect_page.status = 200
        mock_redirect_page.headers = {}

        mock_fetcher.get.side_effect = [mock_page, mock_redirect_page]

        mock_stealthy_instance = MagicMock()
        mock_stealthy_page = MagicMock()
        mock_stealthy_page.status = 200
        mock_stealthy_page.body = '<html><body></body></html>'
        mock_stealthy_instance.fetch.return_value = mock_stealthy_page
        mock_stealthy.return_value = mock_stealthy_instance

        results = search("milk", location_id="12345", max_results=5)

        assert mock_fetcher.get.call_count == 2
        mock_stealthy.assert_called_once()

    @patch('app.publix.search_products.StealthyFetcher')
    @patch('app.publix.search_products.Fetcher')
    def test_handles_redirect_in_fallback_path(self, mock_fetcher, mock_stealthy):
        mock_fail_page = MagicMock()
        mock_fail_page.status = 200
        mock_fail_page.body = '<html><body>Error page</body></html>'

        mock_redirect_page = MagicMock()
        mock_redirect_page.status = 302
        mock_redirect_page.headers = {'location': '/search?searchtermredirect=milk'}

        mock_fetcher.get.side_effect = [mock_fail_page, mock_redirect_page]

        mock_stealthy_instance = MagicMock()
        mock_stealthy_page = MagicMock()
        mock_stealthy_page.status = 200
        mock_stealthy_page.body = '<html><body></body></html>'
        mock_stealthy_instance.fetch.return_value = mock_stealthy_page
        mock_stealthy.return_value = mock_stealthy_instance

        results = search("milk", max_results=5)

        call_args = mock_stealthy_instance.fetch.call_args
        fetched_url = call_args[0][0]
        assert 'searchtermredirect=milk' in fetched_url
        assert 'facet=promoType' in fetched_url

    @patch('app.publix.search_products.StealthyFetcher')
    @patch('app.publix.search_products.Fetcher')
    def test_extracts_products_from_fast_path(self, mock_fetcher, mock_stealthy):
        mock_page = MagicMock()
        mock_page.status = 200
        mock_page.body = '''
            <html>
            <body>
                <a href="/pd/organic-milk/RIO-PCI-111" aria-label="$5.99 - Organic Milk 1 Gallon">Link</a>
                <a href="/pd/whole-milk/RIO-PCI-222" aria-label="$4.49 - Whole Milk 1 Gallon">Link</a>
            </body>
            </html>
        '''
        mock_fetcher.get.return_value = mock_page

        results = search("milk", max_results=5)

        assert len(results) == 2
        assert results[0]['name'] == 'Organic Milk 1 Gallon'
        assert results[0]['price'] == 5.99
        assert results[0]['product_id'] == 'RIO-PCI-111'
        assert results[1]['name'] == 'Whole Milk 1 Gallon'
        assert results[1]['price'] == 4.49
