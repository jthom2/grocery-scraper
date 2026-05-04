from app.matching.brands import classify_brand, normalize_brand


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
