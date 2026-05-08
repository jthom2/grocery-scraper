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


def test_query_without_size_does_not_penalize_candidate_size():
    reference = fingerprint_query("2% milk")
    candidate = _product("Great Value 2% Reduced Fat Milk, 1 Gallon", "Great Value", "walmart")

    result = score_fingerprints(reference, candidate)

    assert result.decision == "equivalent"
    assert not any("missing comparable size" in penalty for penalty in result.penalties)


def test_query_with_size_still_penalizes_missing_candidate_size():
    reference = fingerprint_query("2% milk 1 gallon")
    candidate = _product("Great Value 2% Reduced Fat Milk", "Great Value", "walmart")

    result = score_fingerprints(reference, candidate)

    assert result.decision == "substitute"
    assert any("missing comparable size" in penalty for penalty in result.penalties)


def test_fat_free_milk_matches_skim_milk_without_size():
    reference = fingerprint_query("fat free milk")
    candidate = _product("Great Value Fat-Free Milk, Gallon, 128 fl oz", "Great Value", "walmart")

    result = score_fingerprints(reference, candidate)

    assert result.decision == "equivalent"
    assert result.fingerprint.attributes["fat_level"] == "skim"
    assert not any("missing comparable size" in penalty for penalty in result.penalties)


def test_non_fat_dry_milk_is_not_equivalent_to_fluid_fat_free_milk():
    reference = fingerprint_query("fat free milk")
    candidate = _product("Great Value Instant Non-Fat Dry Milk, 64 oz Bag", "Great Value", "walmart")

    result = score_fingerprints(reference, candidate)

    assert result.decision == "different"
    assert any("form" in penalty for penalty in result.penalties)


def test_branded_query_does_not_equate_to_store_brand_product():
    reference = fingerprint_query("Kraft cheddar cheese 8 oz")
    candidate = _product("Great Value Cheddar Cheese, 8 oz", "Great Value", "walmart")

    result = score_fingerprints(reference, candidate)

    assert result.decision != "equivalent"


def test_greek_yogurt_equivalent_across_retailers():
    reference = _product("Kroger Greek Yogurt Vanilla 32 oz", "Kroger", "kroger")
    candidate = _product("Great Value Greek Yogurt Vanilla 32 oz", "Great Value", "walmart")

    result = score_fingerprints(reference, candidate)

    assert result.decision == "equivalent"


def test_ground_beef_lean_mismatch_is_different():
    reference = _product("Ground Beef 80/20 1 lb", "Great Value", "walmart")
    candidate = _product("Ground Beef 93/7 1 lb", "Great Value", "walmart")

    result = score_fingerprints(reference, candidate)

    assert result.decision == "different"
    assert any("lean_pct" in p for p in result.penalties)


def test_fresh_chicken_is_not_frozen_chicken():
    reference = _product("Chicken Breast Boneless Skinless 2 lb", "Tyson", "walmart")
    candidate = _product("Frozen Chicken Breast Boneless Skinless 2 lb", "Tyson", "walmart")

    result = score_fingerprints(reference, candidate)

    assert result.decision == "different"
    assert any("category" in p for p in result.penalties)


def test_organic_produce_not_equivalent_to_conventional():
    reference = fingerprint_query("organic bananas")
    candidate = _product("Bananas per lb", None, "walmart")

    result = score_fingerprints(reference, candidate)

    # organic mismatch should prevent equivalence
    assert result.decision != "equivalent"


def test_same_pasta_shape_equivalent_across_store_brands():
    reference = _product("Kroger Spaghetti 16 oz", "Kroger", "kroger")
    candidate = _product("Great Value Spaghetti 16 oz", "Great Value", "walmart")

    result = score_fingerprints(reference, candidate)

    assert result.decision == "equivalent"


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

    walmart = response.matches_by_retailer["walmart"]

    assert [item.product["product_id"] for item in walmart.candidates] == ["a", "b"]
