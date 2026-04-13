# ensures pydantic models enforce consistent data shape across retailers
import pytest
from pydantic import ValidationError

from app.models import (
    NormalizedProduct,
    NormalizedLocation,
    normalize_product,
    normalize_location,
)


# validates product normalization catches bad data early
class TestNormalizedProduct:
    # minimal case verifies required fields are actually required
    def test_minimal_valid_product(self, sample_product_data):
        result = normalize_product(sample_product_data)
        assert result["retailer"] == "walmart"
        assert result["name"] == "Test Product"
        assert result["price"] == 9.99

    # retailer apis sometimes return padded strings
    def test_whitespace_stripping(self):
        data = {
            "retailer": "  walmart  ",
            "name": "  Test Product  ",
            "brand": "\t Brand Name \n",
        }
        result = normalize_product(data)
        assert result["retailer"] == "walmart"
        assert result["name"] == "Test Product"
        assert result["brand"] == "Brand Name"

    # catches missing data before it corrupts downstream systems
    def test_missing_required_field_retailer(self):
        with pytest.raises(ValidationError) as exc_info:
            normalize_product({"name": "Test"})
        assert "retailer" in str(exc_info.value)

    # products without names are unusable in display
    def test_missing_required_field_name(self):
        with pytest.raises(ValidationError) as exc_info:
            normalize_product({"retailer": "walmart"})
        assert "name" in str(exc_info.value)

    # forbid extra catches api schema changes early
    def test_extra_fields_forbidden(self):
        data = {
            "retailer": "walmart",
            "name": "Test",
            "unknown_field": "value",
        }
        with pytest.raises(ValidationError) as exc_info:
            normalize_product(data)
        assert "unknown_field" in str(exc_info.value)

    # downstream code expects float not decimal or string
    def test_price_type_coercion_float(self):
        data = {"retailer": "walmart", "name": "Test", "price": 9.99}
        result = normalize_product(data)
        assert result["price"] == 9.99
        assert isinstance(result["price"], float)

    # some apis return integer prices for whole dollar amounts
    def test_price_type_coercion_int(self):
        data = {"retailer": "walmart", "name": "Test", "price": 10}
        result = normalize_product(data)
        assert result["price"] == 10.0

    # some products have no listed price (out of stock, etc)
    def test_price_none_allowed(self):
        data = {"retailer": "walmart", "name": "Test", "price": None}
        result = normalize_product(data)
        assert result["price"] is None

    # in_stock drives filtering and display logic
    def test_in_stock_boolean(self):
        data = {"retailer": "walmart", "name": "Test", "in_stock": True}
        result = normalize_product(data)
        assert result["in_stock"] is True

    # review count is always whole number
    def test_reviews_integer(self):
        data = {"retailer": "walmart", "name": "Test", "reviews": 150}
        result = normalize_product(data)
        assert result["reviews"] == 150

    # empty dict easier to work with than none
    def test_metadata_default_empty_dict(self):
        data = {"retailer": "walmart", "name": "Test"}
        result = normalize_product(data)
        assert result["metadata"] == {}

    # metadata stores retailer-specific fields not in schema
    def test_metadata_preserves_data(self):
        meta = {"raw_price": "USD 9.99", "nested": {"key": "value"}}
        data = {"retailer": "walmart", "name": "Test", "metadata": meta}
        result = normalize_product(data)
        assert result["metadata"] == meta

    # sparse data should not crash normalization
    def test_all_optional_fields_none(self):
        data = {
            "retailer": "walmart",
            "name": "Test",
            "product_id": None,
            "location_id": None,
            "brand": None,
            "size": None,
            "price": None,
            "price_display": None,
            "unit_price": None,
            "promo_price": None,
            "was_price": None,
            "rating": None,
            "reviews": None,
            "image_url": None,
            "in_stock": None,
            "availability": None,
            "stock_level": None,
            "url": None,
            "description": None,
        }
        result = normalize_product(data)
        assert result["retailer"] == "walmart"
        assert result["price"] is None

    # ratings are typically x.x format
    def test_rating_float(self):
        data = {"retailer": "walmart", "name": "Test", "rating": 4.5}
        result = normalize_product(data)
        assert result["rating"] == 4.5


# validates location normalization catches bad data early
class TestNormalizedLocation:
    # minimal case verifies required fields are actually required
    def test_minimal_valid_location(self, sample_location_data):
        result = normalize_location(sample_location_data)
        assert result["retailer"] == "walmart"
        assert result["location_id"] == "5678"
        assert result["name"] == "Test Store"

    # catches missing data before it corrupts downstream systems
    def test_missing_required_field_retailer(self):
        with pytest.raises(ValidationError) as exc_info:
            normalize_location({"location_id": "123", "name": "Store"})
        assert "retailer" in str(exc_info.value)

    # location_id needed for store-scoped searches
    def test_missing_required_field_location_id(self):
        with pytest.raises(ValidationError) as exc_info:
            normalize_location({"retailer": "walmart", "name": "Store"})
        assert "location_id" in str(exc_info.value)

    # name needed for display in store selection
    def test_missing_required_field_name(self):
        with pytest.raises(ValidationError) as exc_info:
            normalize_location({"retailer": "walmart", "location_id": "123"})
        assert "name" in str(exc_info.value)

    # coordinates used for distance calculations
    def test_latitude_longitude_float(self):
        data = {
            "retailer": "walmart",
            "location_id": "123",
            "name": "Store",
            "latitude": 40.7128,
            "longitude": -74.0060,
        }
        result = normalize_location(data)
        assert result["latitude"] == 40.7128
        assert result["longitude"] == -74.0060

    # is_open drives filtering for open-now searches
    def test_is_open_boolean(self):
        data = {
            "retailer": "kroger",
            "location_id": "123",
            "name": "Store",
            "is_open": True,
        }
        result = normalize_location(data)
        assert result["is_open"] is True

    # forbid extra catches api schema changes early
    def test_extra_fields_forbidden(self):
        data = {
            "retailer": "walmart",
            "location_id": "123",
            "name": "Store",
            "unknown_field": "value",
        }
        with pytest.raises(ValidationError) as exc_info:
            normalize_location(data)
        assert "unknown_field" in str(exc_info.value)

    # retailer apis sometimes return padded strings
    def test_whitespace_stripping_location(self):
        data = {
            "retailer": "  kroger  ",
            "location_id": "  456  ",
            "name": "  Store Name  ",
        }
        result = normalize_location(data)
        assert result["retailer"] == "kroger"
        assert result["location_id"] == "456"
        assert result["name"] == "Store Name"

    # empty dict easier to work with than none
    def test_metadata_default_empty_dict(self):
        data = {"retailer": "walmart", "location_id": "123", "name": "Store"}
        result = normalize_location(data)
        assert result["metadata"] == {}


# verifies functions return dicts for json serialization
class TestNormalizeFunctions:
    # dict is more portable than pydantic model
    def test_normalize_product_returns_dict(self, sample_product_data):
        result = normalize_product(sample_product_data)
        assert isinstance(result, dict)
        assert not isinstance(result, NormalizedProduct)

    # dict is more portable than pydantic model
    def test_normalize_location_returns_dict(self, sample_location_data):
        result = normalize_location(sample_location_data)
        assert isinstance(result, dict)
        assert not isinstance(result, NormalizedLocation)
