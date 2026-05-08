from app.matching.normalizer import fingerprint_product, fingerprint_query
from app.matching.scorer import score_fingerprints
from app.matching.service import match_products


def _product(name, brand, retailer="walmart", size=None):
    return fingerprint_product({
        "retailer": retailer,
        "product_id": name.lower().replace(" ", "-"),
        "name": name,
        "brand": brand,
        "size": size,
    })


def test_store_brand_two_percent_milk_is_equivalent_across_retailers():
    reference = _product("Great Value 2% Reduced Fat Milk, 1 Gallon", "Great Value", "walmart")
    candidate = _product("Kroger 2% Reduced Fat Milk, 1 gal", "Kroger", "kroger")

    result = score_fingerprints(reference, candidate)

    assert result.decision == "equivalent"
    assert result.score >= 0.82


def test_whole_milk_is_not_equivalent_to_two_percent_milk():
    reference = _product("Great Value Whole Milk, 1 Gallon", "Great Value", "walmart")
    candidate = _product("Great Value 2% Reduced Fat Milk, 1 Gallon", "Great Value", "walmart")

    result = score_fingerprints(reference, candidate)

    assert result.decision == "different"
    assert any("fat_level" in penalty for penalty in result.penalties)


def test_store_brand_large_eggs_are_equivalent_across_retailers():
    reference = _product("Publix Large White Eggs, 12 ct", "Publix", "publix")
    candidate = _product("Kroger Large Eggs, Dozen", "Kroger", "kroger")

    result = score_fingerprints(reference, candidate)

    assert result.decision == "equivalent"


def test_unsalted_butter_is_not_equivalent_to_salted_butter():
    reference = _product("Publix Unsalted Butter Sticks, 1 lb", "Publix", "publix")
    candidate = _product("Kroger Salted Butter Sticks, 16 oz", "Kroger", "kroger")

    result = score_fingerprints(reference, candidate)

    assert result.decision == "different"
    assert any("salt" in penalty for penalty in result.penalties)


def test_shredded_cheddar_is_not_equivalent_to_sliced_cheddar():
    reference = _product("Great Value Shredded Cheddar Cheese, 8 oz", "Great Value", "walmart")
    candidate = _product("Kroger Sliced Cheddar Cheese, 8 oz", "Kroger", "kroger")

    result = score_fingerprints(reference, candidate)

    assert result.decision == "different"
    assert any("form" in penalty for penalty in result.penalties)


def test_national_brand_cereal_is_not_equivalent_to_store_brand_cereal():
    reference = _product("Cheerios Cereal, 18 oz", "Cheerios", "walmart")
    candidate = _product("Great Value Toasted Oats Cereal, 18 oz", "Great Value", "walmart")

    result = score_fingerprints(reference, candidate)

    assert result.decision == "different"


def test_national_brand_exact_match_is_equivalent_across_retailers():
    reference = _product("Cheerios Original Cereal, 18 oz", "Cheerios", "walmart")
    candidate = _product("Cheerios Original Cereal, 18 oz", "Cheerios", "kroger")

    result = score_fingerprints(reference, candidate)

    assert result.decision == "equivalent"


def test_packaged_good_requires_high_token_similarity_for_equivalence():
    reference = _product("Cheerios Original Cereal, 18 oz", "Cheerios", "walmart")
    candidate = _product("Cheerios Honey Nut Cereal, 18 oz", "Cheerios", "kroger")

    result = score_fingerprints(reference, candidate)

    assert result.decision != "equivalent"
    assert any("token similarity" in penalty for penalty in result.penalties)


def test_generic_packaged_query_can_match_exact_national_brand_product():
    reference = fingerprint_query("Cheerios Original Cereal 18 oz")
    candidate = _product("Cheerios Original Cereal, 18 oz", "Cheerios", "walmart")

    result = score_fingerprints(reference, candidate)

    assert result.decision == "equivalent"


def test_generic_query_can_match_store_brand_product():
    reference = fingerprint_query("2% milk 1 gallon")
    candidate = _product("Great Value 2% Reduced Fat Milk, 1 Gallon", "Great Value", "walmart")

    result = score_fingerprints(reference, candidate)

    assert result.decision == "equivalent"


def test_token_aliases_support_equivalent_milk_descriptions():
    reference = fingerprint_query("2 percent milk 1 gallon")
    candidate = _product("Great Value 2% Reduced Fat Milk, 1 gal", "Great Value", "walmart")

    result = score_fingerprints(reference, candidate)

    assert result.decision == "equivalent"


def test_missing_size_is_not_equivalent():
    reference = fingerprint_query("2% milk")
    candidate = _product("Great Value 2% Reduced Fat Milk, 1 Gallon", "Great Value", "walmart")

    result = score_fingerprints(reference, candidate)

    assert result.decision == "substitute"
    assert any("missing comparable size" in penalty for penalty in result.penalties)


def test_branded_query_does_not_equate_to_store_brand_product():
    reference = fingerprint_query("Kraft cheddar cheese 8 oz")
    candidate = _product("Great Value Cheddar Cheese, 8 oz", "Great Value", "walmart")

    result = score_fingerprints(reference, candidate)

    assert result.decision != "equivalent"


def test_match_products_uses_deterministic_tie_sort():
    products = [
        {
            "retailer": "walmart",
            "product_id": "b",
            "name": "Great Value 2% Reduced Fat Milk, 1 Gallon",
            "brand": "Great Value",
        },
        {
            "retailer": "walmart",
            "product_id": "a",
            "name": "Great Value 2% Reduced Fat Milk, 1 Gallon",
            "brand": "Great Value",
        },
    ]

    response = match_products("2% milk 1 gallon", products)

    assert [item.product["product_id"] for item in response.equivalent] == ["a", "b"]
