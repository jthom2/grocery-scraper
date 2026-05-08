from app.matching.normalizer import (
    detect_category,
    extract_attributes,
    fingerprint_product,
    normalize_text,
    tokenize,
)


# --- category detection ---


def test_yogurt_detected():
    assert detect_category(tokenize("Greek yogurt vanilla")) == "yogurt"


def test_juice_detected():
    assert detect_category(tokenize("orange juice not from concentrate")) == "juice"


def test_coffee_detected():
    assert detect_category(tokenize("Folgers medium roast ground coffee")) == "coffee"


def test_pasta_detected_by_shape():
    assert detect_category(tokenize("Barilla spaghetti 16 oz")) == "pasta"
    assert detect_category(tokenize("penne rigate pasta")) == "pasta"


def test_rice_detected():
    assert detect_category(tokenize("jasmine rice 5 lb")) == "rice"


def test_chicken_detected():
    assert detect_category(tokenize("boneless skinless chicken breast")) == "chicken"


def test_beef_detected():
    assert detect_category(tokenize("ground beef 80/20 1 lb")) == "beef"


def test_pork_detected():
    assert detect_category(tokenize("pork tenderloin 1.5 lb")) == "pork"


def test_produce_detected():
    assert detect_category(tokenize("organic bananas")) == "produce"
    assert detect_category(tokenize("avocado each")) == "produce"
    assert detect_category(tokenize("russet potatoes 5 lb bag")) == "produce"


def test_frozen_standalone_detected():
    assert detect_category(tokenize("frozen pizza 12 inch")) == "frozen"


def test_frozen_overrides_meat_category():
    # frozen chicken breast -> frozen, not chicken
    assert detect_category(tokenize("frozen chicken breast 2 lb")) == "frozen"


def test_frozen_overrides_produce_category():
    assert detect_category(tokenize("frozen strawberries 16 oz")) == "frozen"


def test_water_detected():
    assert detect_category(tokenize("purified water 24 pack")) == "water"


def test_snacks_detected():
    assert detect_category(tokenize("Lays potato chips 10 oz")) == "snacks"
    assert detect_category(tokenize("microwave popcorn 3 ct")) == "snacks"


def test_paper_goods_detected():
    assert detect_category(tokenize("paper towel 6 roll")) == "paper_goods"


# --- yogurt attributes ---


def test_yogurt_greek_style():
    text = normalize_text("Chobani Greek Yogurt Vanilla")
    tokens = tokenize("Chobani Greek Yogurt Vanilla")
    attrs = extract_attributes("yogurt", text, tokens)
    assert attrs["style"] == "greek"
    assert attrs["flavor"] == "vanilla"


def test_yogurt_regular_style():
    text = normalize_text("Yoplait Original Yogurt Strawberry")
    tokens = tokenize("Yoplait Original Yogurt Strawberry")
    attrs = extract_attributes("yogurt", text, tokens)
    assert attrs["style"] == "regular"
    assert attrs["flavor"] == "strawberry"


def test_yogurt_nonfat():
    text = normalize_text("Fat Free Greek Yogurt Plain")
    tokens = tokenize("Fat Free Greek Yogurt Plain")
    attrs = extract_attributes("yogurt", text, tokens)
    assert attrs["fat_level"] == "nonfat"
    assert attrs["flavor"] == "plain"


# --- juice attributes ---


def test_juice_orange_not_from_concentrate():
    text = normalize_text("Tropicana Pure Premium Orange Juice Not From Concentrate")
    tokens = tokenize("Tropicana Pure Premium Orange Juice Not From Concentrate")
    attrs = extract_attributes("juice", text, tokens)
    assert attrs["fruit"] == "orange"
    assert attrs["concentrate"] == "not_from_concentrate"


def test_juice_apple():
    text = normalize_text("Great Value 100% Apple Juice 64 fl oz")
    tokens = tokenize("Great Value 100% Apple Juice 64 fl oz")
    attrs = extract_attributes("juice", text, tokens)
    assert attrs["fruit"] == "apple"


# --- coffee attributes ---


def test_coffee_dark_roast_ground():
    text = normalize_text("Folgers Black Silk Dark Roast Ground Coffee")
    tokens = tokenize("Folgers Black Silk Dark Roast Ground Coffee")
    attrs = extract_attributes("coffee", text, tokens)
    assert attrs["roast"] == "dark"
    assert attrs["form"] == "ground"
    assert attrs["decaf"] is False


def test_coffee_decaf():
    text = normalize_text("Starbucks Decaf Medium Roast Whole Bean Coffee")
    tokens = tokenize("Starbucks Decaf Medium Roast Whole Bean Coffee")
    attrs = extract_attributes("coffee", text, tokens)
    assert attrs["decaf"] is True
    assert attrs["roast"] == "medium"
    assert attrs["form"] == "whole_bean"


# --- chicken attributes ---


def test_chicken_breast_boneless_skinless():
    text = normalize_text("Tyson Boneless Skinless Chicken Breast 2.5 lb")
    tokens = tokenize("Tyson Boneless Skinless Chicken Breast 2.5 lb")
    attrs = extract_attributes("chicken", text, tokens)
    assert attrs["cut"] == "breast"
    assert attrs["boneless"] is True
    assert attrs["skinless"] is True
    assert attrs["fresh_or_frozen"] == "fresh"


def test_chicken_frozen():
    text = normalize_text("Frozen Chicken Thighs 3 lb")
    tokens = tokenize("Frozen Chicken Thighs 3 lb")
    attrs = extract_attributes("frozen", text, tokens)
    assert attrs["frozen"] is True


# --- beef attributes ---


def test_beef_ground_with_lean_percentage():
    text = normalize_text("Ground Beef 80/20 1 lb")
    tokens = tokenize("Ground Beef 80/20 1 lb")
    attrs = extract_attributes("beef", text, tokens)
    assert attrs["cut"] == "ground"
    assert attrs["lean_pct"] == 80


def test_beef_ground_percent_lean():
    text = normalize_text("93% Lean Ground Beef 1 lb")
    tokens = tokenize("93% Lean Ground Beef 1 lb")
    attrs = extract_attributes("beef", text, tokens)
    assert attrs["lean_pct"] == 93


def test_beef_grass_fed():
    text = normalize_text("Grass-Fed Ground Beef 85/15 16 oz")
    tokens = tokenize("Grass-Fed Ground Beef 85/15 16 oz")
    attrs = extract_attributes("beef", text, tokens)
    assert attrs["grass_fed"] is True


# --- pork attributes ---


def test_pork_tenderloin():
    text = normalize_text("Pork Tenderloin 1.5 lb")
    tokens = tokenize("Pork Tenderloin 1.5 lb")
    attrs = extract_attributes("pork", text, tokens)
    assert attrs["cut"] == "tenderloin"
    assert attrs["fresh_or_frozen"] == "fresh"


# --- produce attributes ---


def test_produce_organic():
    text = normalize_text("Organic Bananas")
    tokens = tokenize("Organic Bananas")
    attrs = extract_attributes("produce", text, tokens)
    assert attrs["organic"] is True


def test_produce_conventional():
    text = normalize_text("Bananas")
    tokens = tokenize("Bananas")
    attrs = extract_attributes("produce", text, tokens)
    assert attrs["organic"] is False


# --- pasta attributes ---


def test_pasta_spaghetti():
    text = normalize_text("Barilla Spaghetti No. 5 16 oz")
    tokens = tokenize("Barilla Spaghetti No. 5 16 oz")
    attrs = extract_attributes("pasta", text, tokens)
    assert attrs["shape"] == "spaghetti"
    assert attrs["organic"] is False


def test_pasta_whole_wheat_penne():
    text = normalize_text("Barilla Whole Wheat Penne 13.25 oz")
    tokens = tokenize("Barilla Whole Wheat Penne 13.25 oz")
    attrs = extract_attributes("pasta", text, tokens)
    assert attrs["shape"] == "penne"
    assert attrs["whole_wheat"] is True


# --- rice attributes ---


def test_rice_jasmine():
    text = normalize_text("Thai Jasmine Rice 5 lb")
    tokens = tokenize("Thai Jasmine Rice 5 lb")
    attrs = extract_attributes("rice", text, tokens)
    assert attrs["variety"] == "jasmine"


def test_rice_brown():
    text = normalize_text("Lundberg Organic Brown Rice 2 lb")
    tokens = tokenize("Lundberg Organic Brown Rice 2 lb")
    attrs = extract_attributes("rice", text, tokens)
    assert attrs["variety"] == "brown"
    assert attrs["organic"] is True


# --- paper goods attributes ---


def test_paper_goods_paper_towel():
    text = normalize_text("Bounty Paper Towels 6 Roll")
    tokens = tokenize("Bounty Paper Towels 6 Roll")
    attrs = extract_attributes("paper_goods", text, tokens)
    assert attrs["type"] == "paper_towel"


def test_paper_goods_toilet_paper():
    text = normalize_text("Charmin Ultra Soft Toilet Paper 12 Roll")
    tokens = tokenize("Charmin Ultra Soft Toilet Paper 12 Roll")
    attrs = extract_attributes("paper_goods", text, tokens)
    assert attrs["type"] == "toilet_paper"


# --- fingerprint integration ---


def test_fingerprint_product_detects_yogurt_category():
    fp = fingerprint_product({
        "retailer": "kroger",
        "product_id": "y1",
        "name": "Kroger Greek Yogurt Vanilla 32 oz",
        "brand": "Kroger",
    })
    assert fp.category == "yogurt"
    assert fp.attributes["style"] == "greek"


def test_fingerprint_product_detects_chicken_category():
    fp = fingerprint_product({
        "retailer": "walmart",
        "product_id": "c1",
        "name": "Tyson Boneless Skinless Chicken Breast 2.5 lb",
        "brand": "Tyson",
    })
    assert fp.category == "chicken"
    assert fp.attributes["cut"] == "breast"
    assert fp.brand_class == "national_brand"


def test_fingerprint_product_detects_frozen_override():
    fp = fingerprint_product({
        "retailer": "aldi",
        "product_id": "f1",
        "name": "Kirkwood Frozen Chicken Breast 3 lb",
        "brand": "Kirkwood",
    })
    assert fp.category == "frozen"
