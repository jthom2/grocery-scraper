"""Unit tests for Walmart cookie building."""
import base64
import json
import uuid
from urllib.parse import unquote

import pytest

from app.utils.build_cookies import build_location_cookies


class TestBuildLocationCookies:
    """Test Walmart location cookie generation."""

    def test_returns_required_keys(self):
        """Cookie dict contains all required keys."""
        cookies = build_location_cookies("12345", "90210")
        required_keys = {
            "ACID",
            "hasACID",
            "hasLocData",
            "assortmentStoreId",
            "locGuestData",
            "locDataV3",
        }
        assert required_keys == set(cookies.keys())

    def test_store_id_in_assortment_store_id(self):
        """assortmentStoreId matches input store_id."""
        cookies = build_location_cookies("99999", "90210")
        assert cookies["assortmentStoreId"] == "99999"

    def test_acid_is_uuid_format(self):
        """ACID is a valid UUID string."""
        cookies = build_location_cookies("123", "90210")
        parsed = uuid.UUID(cookies["ACID"])
        assert str(parsed) == cookies["ACID"]

    def test_has_acid_is_true_string(self):
        """hasACID is string 'true'."""
        cookies = build_location_cookies("123", "90210")
        assert cookies["hasACID"] == "true"

    def test_has_loc_data_is_one_string(self):
        """hasLocData is string '1'."""
        cookies = build_location_cookies("123", "90210")
        assert cookies["hasLocData"] == "1"

    def test_loc_guest_data_is_valid_base64(self):
        """locGuestData is URL-encoded base64."""
        cookies = build_location_cookies("123", "90210")
        decoded_b64 = unquote(cookies["locGuestData"])
        raw_json = base64.b64decode(decoded_b64).decode("utf-8")
        payload = json.loads(raw_json)

        assert payload["pickup"]["nodeId"] == "123"
        assert payload["postalCode"]["base"] == "90210"

    def test_loc_data_v3_matches_loc_guest_data(self):
        """locDataV3 equals locGuestData."""
        cookies = build_location_cookies("123", "90210")
        assert cookies["locDataV3"] == cookies["locGuestData"]

    def test_payload_contains_timestamps(self):
        """Payload contains timestamp fields."""
        cookies = build_location_cookies("123", "90210")
        decoded_b64 = unquote(cookies["locGuestData"])
        raw_json = base64.b64decode(decoded_b64).decode("utf-8")
        payload = json.loads(raw_json)

        assert "timestamp" in payload["pickup"]
        assert "timestamp" in payload["postalCode"]
        assert isinstance(payload["pickup"]["timestamp"], int)

    def test_payload_validate_key_contains_acid(self):
        """validateKey contains the ACID value."""
        cookies = build_location_cookies("123", "90210")
        decoded_b64 = unquote(cookies["locGuestData"])
        raw_json = base64.b64decode(decoded_b64).decode("utf-8")
        payload = json.loads(raw_json)

        assert cookies["ACID"] in payload["validateKey"]
        assert payload["validateKey"].startswith("prod:v2:")

    def test_different_store_ids_produce_different_cookies(self):
        """Different store IDs produce different cookie values."""
        cookies1 = build_location_cookies("111", "90210")
        cookies2 = build_location_cookies("222", "90210")

        assert cookies1["assortmentStoreId"] != cookies2["assortmentStoreId"]
        assert cookies1["locGuestData"] != cookies2["locGuestData"]

    def test_different_zip_codes_produce_different_cookies(self):
        """Different ZIP codes produce different cookie values."""
        cookies1 = build_location_cookies("123", "90210")
        cookies2 = build_location_cookies("123", "10001")

        decoded1 = unquote(cookies1["locGuestData"])
        decoded2 = unquote(cookies2["locGuestData"])

        payload1 = json.loads(base64.b64decode(decoded1).decode("utf-8"))
        payload2 = json.loads(base64.b64decode(decoded2).decode("utf-8"))

        assert payload1["postalCode"]["base"] == "90210"
        assert payload2["postalCode"]["base"] == "10001"
