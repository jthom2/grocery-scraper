# ensures cookies match walmart's expected format for location scoping
import base64
import json
import uuid
from urllib.parse import unquote

import pytest

from app.utils.build_cookies import build_location_cookies


# location cookies enable store-specific product availability
class TestBuildLocationCookies:
    # walmart expects specific cookie keys for store context
    def test_returns_required_keys(self):
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

    # assortment id controls which products appear in results
    def test_store_id_in_assortment_store_id(self):
        cookies = build_location_cookies("99999", "90210")
        assert cookies["assortmentStoreId"] == "99999"

    # walmart validates acid format server-side
    def test_acid_is_uuid_format(self):
        cookies = build_location_cookies("123", "90210")
        parsed = uuid.UUID(cookies["ACID"])
        assert str(parsed) == cookies["ACID"]

    # boolean-like flags are strings not booleans in walmart cookies
    def test_has_acid_is_true_string(self):
        cookies = build_location_cookies("123", "90210")
        assert cookies["hasACID"] == "true"

    # boolean-like flags are strings not booleans in walmart cookies
    def test_has_loc_data_is_one_string(self):
        cookies = build_location_cookies("123", "90210")
        assert cookies["hasLocData"] == "1"

    # walmart encodes location json as base64 in cookie value
    def test_loc_guest_data_is_valid_base64(self):
        cookies = build_location_cookies("123", "90210")
        decoded_b64 = unquote(cookies["locGuestData"])
        raw_json = base64.b64decode(decoded_b64).decode("utf-8")
        payload = json.loads(raw_json)

        assert payload["pickup"]["nodeId"] == "123"
        assert payload["postalCode"]["base"] == "90210"

    # v3 appears to be redundant but walmart checks both
    def test_loc_data_v3_matches_loc_guest_data(self):
        cookies = build_location_cookies("123", "90210")
        assert cookies["locDataV3"] == cookies["locGuestData"]

    # timestamps may be used for cache invalidation
    def test_payload_contains_timestamps(self):
        cookies = build_location_cookies("123", "90210")
        decoded_b64 = unquote(cookies["locGuestData"])
        raw_json = base64.b64decode(decoded_b64).decode("utf-8")
        payload = json.loads(raw_json)

        assert "timestamp" in payload["pickup"]
        assert "timestamp" in payload["postalCode"]
        assert isinstance(payload["pickup"]["timestamp"], int)

    # validate key links acid to payload for integrity check
    def test_payload_validate_key_contains_acid(self):
        cookies = build_location_cookies("123", "90210")
        decoded_b64 = unquote(cookies["locGuestData"])
        raw_json = base64.b64decode(decoded_b64).decode("utf-8")
        payload = json.loads(raw_json)

        assert cookies["ACID"] in payload["validateKey"]
        assert payload["validateKey"].startswith("prod:v2:")

    # ensures store_id isn't accidentally hardcoded
    def test_different_store_ids_produce_different_cookies(self):
        cookies1 = build_location_cookies("111", "90210")
        cookies2 = build_location_cookies("222", "90210")

        assert cookies1["assortmentStoreId"] != cookies2["assortmentStoreId"]
        assert cookies1["locGuestData"] != cookies2["locGuestData"]

    # ensures zip_code isn't accidentally hardcoded
    def test_different_zip_codes_produce_different_cookies(self):
        cookies1 = build_location_cookies("123", "90210")
        cookies2 = build_location_cookies("123", "10001")

        decoded1 = unquote(cookies1["locGuestData"])
        decoded2 = unquote(cookies2["locGuestData"])

        payload1 = json.loads(base64.b64decode(decoded1).decode("utf-8"))
        payload2 = json.loads(base64.b64decode(decoded2).decode("utf-8"))

        assert payload1["postalCode"]["base"] == "90210"
        assert payload2["postalCode"]["base"] == "10001"
