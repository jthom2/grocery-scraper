"""Unit tests for app.models - Pydantic normalization."""
import pytest
from pydantic import ValidationError

from app.models import (
    NormalizedProduct,
    NormalizedLocation,
    normalize_product,
    normalize_location,
)


class TestNormalizedProduct:
    """Test NormalizedProduct model validation."""

    def test_minimal_valid_product(self, sample_product_data):
        """Product with only required fields."""
        result = normalize_product(sample_product_data)
        assert result["retailer"] == "walmart"
        assert result["name"] == "Test Product"
        assert result["price"] == 9.99

    def test_whitespace_stripping(self):
        """Whitespace is stripped from string fields."""
        data = {
            "retailer": "  walmart  ",
            "name": "  Test Product  ",
            "brand": "\t Brand Name \n",
        }
        result = normalize_product(data)
        assert result["retailer"] == "walmart"
        assert result["name"] == "Test Product"
        assert result["brand"] == "Brand Name"

    def test_missing_required_field_retailer(self):
        """Missing retailer raises ValidationError."""
        with pytest.raises(ValidationError) as exc_info:
            normalize_product({"name": "Test"})
        assert "retailer" in str(exc_info.value)

    def test_missing_required_field_name(self):
        """Missing name raises ValidationError."""
        with pytest.raises(ValidationError) as exc_info:
            normalize_product({"retailer": "walmart"})
        assert "name" in str(exc_info.value)

    def test_extra_fields_forbidden(self):
        """Extra fields raise ValidationError (extra='forbid')."""
        data = {
            "retailer": "walmart",
            "name": "Test",
            "unknown_field": "value",
        }
        with pytest.raises(ValidationError) as exc_info:
            normalize_product(data)
        assert "unknown_field" in str(exc_info.value)

    def test_price_type_coercion_float(self):
        """Price accepts float values."""
        data = {"retailer": "walmart", "name": "Test", "price": 9.99}
        result = normalize_product(data)
        assert result["price"] == 9.99
        assert isinstance(result["price"], float)

    def test_price_type_coercion_int(self):
        """Price coerces int to float."""
        data = {"retailer": "walmart", "name": "Test", "price": 10}
        result = normalize_product(data)
        assert result["price"] == 10.0

    def test_price_none_allowed(self):
        """Price can be None."""
        data = {"retailer": "walmart", "name": "Test", "price": None}
        result = normalize_product(data)
        assert result["price"] is None

    def test_in_stock_boolean(self):
        """in_stock accepts boolean values."""
        data = {"retailer": "walmart", "name": "Test", "in_stock": True}
        result = normalize_product(data)
        assert result["in_stock"] is True

    def test_reviews_integer(self):
        """reviews field accepts integers."""
        data = {"retailer": "walmart", "name": "Test", "reviews": 150}
        result = normalize_product(data)
        assert result["reviews"] == 150

    def test_metadata_default_empty_dict(self):
        """metadata defaults to empty dict."""
        data = {"retailer": "walmart", "name": "Test"}
        result = normalize_product(data)
        assert result["metadata"] == {}

    def test_metadata_preserves_data(self):
        """metadata preserves arbitrary nested data."""
        meta = {"raw_price": "USD 9.99", "nested": {"key": "value"}}
        data = {"retailer": "walmart", "name": "Test", "metadata": meta}
        result = normalize_product(data)
        assert result["metadata"] == meta

    def test_all_optional_fields_none(self):
        """All optional fields can be None."""
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

    def test_rating_float(self):
        """rating accepts float values."""
        data = {"retailer": "walmart", "name": "Test", "rating": 4.5}
        result = normalize_product(data)
        assert result["rating"] == 4.5


class TestNormalizedLocation:
    """Test NormalizedLocation model validation."""

    def test_minimal_valid_location(self, sample_location_data):
        """Location with only required fields."""
        result = normalize_location(sample_location_data)
        assert result["retailer"] == "walmart"
        assert result["location_id"] == "5678"
        assert result["name"] == "Test Store"

    def test_missing_required_field_retailer(self):
        """Missing retailer raises ValidationError."""
        with pytest.raises(ValidationError) as exc_info:
            normalize_location({"location_id": "123", "name": "Store"})
        assert "retailer" in str(exc_info.value)

    def test_missing_required_field_location_id(self):
        """Missing location_id raises ValidationError."""
        with pytest.raises(ValidationError) as exc_info:
            normalize_location({"retailer": "walmart", "name": "Store"})
        assert "location_id" in str(exc_info.value)

    def test_missing_required_field_name(self):
        """Missing name raises ValidationError."""
        with pytest.raises(ValidationError) as exc_info:
            normalize_location({"retailer": "walmart", "location_id": "123"})
        assert "name" in str(exc_info.value)

    def test_latitude_longitude_float(self):
        """Coordinates accept float values."""
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

    def test_is_open_boolean(self):
        """is_open accepts boolean values."""
        data = {
            "retailer": "kroger",
            "location_id": "123",
            "name": "Store",
            "is_open": True,
        }
        result = normalize_location(data)
        assert result["is_open"] is True

    def test_extra_fields_forbidden(self):
        """Extra fields raise ValidationError."""
        data = {
            "retailer": "walmart",
            "location_id": "123",
            "name": "Store",
            "unknown_field": "value",
        }
        with pytest.raises(ValidationError) as exc_info:
            normalize_location(data)
        assert "unknown_field" in str(exc_info.value)

    def test_whitespace_stripping_location(self):
        """Whitespace is stripped from string fields."""
        data = {
            "retailer": "  kroger  ",
            "location_id": "  456  ",
            "name": "  Store Name  ",
        }
        result = normalize_location(data)
        assert result["retailer"] == "kroger"
        assert result["location_id"] == "456"
        assert result["name"] == "Store Name"

    def test_metadata_default_empty_dict(self):
        """metadata defaults to empty dict."""
        data = {"retailer": "walmart", "location_id": "123", "name": "Store"}
        result = normalize_location(data)
        assert result["metadata"] == {}


class TestNormalizeFunctions:
    """Test normalize_product and normalize_location return dicts."""

    def test_normalize_product_returns_dict(self, sample_product_data):
        """normalize_product returns dict, not Pydantic model."""
        result = normalize_product(sample_product_data)
        assert isinstance(result, dict)
        assert not isinstance(result, NormalizedProduct)

    def test_normalize_location_returns_dict(self, sample_location_data):
        """normalize_location returns dict, not Pydantic model."""
        result = normalize_location(sample_location_data)
        assert isinstance(result, dict)
        assert not isinstance(result, NormalizedLocation)
