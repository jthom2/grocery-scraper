from app.matching.brands import classify_brand, infer_brand, normalize_brand


def test_store_brands_classify_as_store_brand():
    assert classify_brand("Great Value", "walmart") == "store_brand"
    assert classify_brand("Kroger", "kroger") == "store_brand"
    assert classify_brand("Publix", "publix") == "store_brand"
    assert classify_brand("Friendly Farms", "aldi") == "store_brand"


def test_unknown_brand_is_unknown():
    assert classify_brand(None, "walmart") == "unknown"


def test_non_store_brand_classifies_as_national_brand():
    assert classify_brand("Cheerios", "walmart") == "national_brand"


def test_brand_normalization_removes_extra_spacing_and_case():
    assert normalize_brand("  Great   Value  ") == "great value"


def test_brand_normalization_canonicalizes_punctuation_variants():
    assert normalize_brand("Sam's Choice") == "sams choice"
    assert normalize_brand("Dave's Killer Bread") == "daves killer bread"


def test_brand_aliases_classify_as_canonical_brand():
    assert classify_brand("Great Value Brand", "walmart") == "store_brand"
    assert classify_brand("Kroger Brand", "kroger") == "store_brand"


def test_brand_inference_uses_safe_prefix_only():
    assert infer_brand("Dave's Killer Bread Thin-Sliced Organic Bread") == "daves killer bread"
    assert infer_brand("Organic Dave's Killer Bread Style Loaf") is None


def test_new_national_brands_classify_correctly():
    assert classify_brand("Chobani", "walmart") == "national_brand"
    assert classify_brand("Barilla", "kroger") == "national_brand"
    assert classify_brand("Tyson", "walmart") == "national_brand"
    assert classify_brand("Bounty", "walmart") == "national_brand"


def test_expanded_store_brands_classify_correctly():
    assert classify_brand("Kirkwood", "aldi") == "store_brand"
    assert classify_brand("Heritage Farm", "kroger") == "store_brand"
    assert classify_brand("Brookdale", "aldi") == "store_brand"
    assert classify_brand("Parents Choice", "walmart") == "store_brand"
