from app.matching.service import match_products


def test_similarity_ranking_prefers_near_exact_milk_match():
    response = match_products(
        "2% milk gallon",
        [
            {
                "retailer": "walmart",
                "product_id": "whole",
                "name": "Great Value Whole Vitamin D Milk, Gallon",
                "brand": "Great Value",
            },
            {
                "retailer": "walmart",
                "product_id": "organic",
                "name": "Great Value Organic Reduced Fat 2% Milk, 1 Gallon, 128 fl oz",
                "brand": "Great Value",
            },
            {
                "retailer": "walmart",
                "product_id": "match",
                "name": "Great Value, 2% Reduced Fat Milk, Gallon",
                "brand": "Great Value",
            },
            {
                "retailer": "walmart",
                "product_id": "coffee",
                "name": "Barissimo Cinnamon Roll Coffee Creamer",
                "brand": "Barissimo",
                "size": "32 fl oz",
            },
        ],
        retailers=["walmart"],
    )

    walmart = response.matches_by_retailer["walmart"]

    assert walmart.status == "equivalent"
    assert walmart.best.product["product_id"] == "match"
    assert walmart.candidates[0].product["product_id"] == "match"
    assert walmart.candidates[0].rank_score > walmart.candidates[1].rank_score


def test_match_products_dedupes_by_retailer_and_product_id():
    response = match_products(
        "2% milk gallon",
        [
            {
                "retailer": "walmart",
                "product_id": "same",
                "name": "Unrelated Product",
                "brand": "Great Value",
            },
            {
                "retailer": "walmart",
                "product_id": "same",
                "name": "Great Value, 2% Reduced Fat Milk, Gallon",
                "brand": "Great Value",
            },
        ],
        retailers=["walmart"],
    )

    walmart = response.matches_by_retailer["walmart"]

    assert len(walmart.candidates) == 1
    assert walmart.candidates[0].product["name"] == "Great Value, 2% Reduced Fat Milk, Gallon"


def test_best_is_null_when_all_candidates_are_different():
    response = match_products(
        "2% milk gallon",
        [
            {
                "retailer": "aldi",
                "product_id": "coffee",
                "name": "Barissimo Cinnamon Roll Coffee Creamer",
                "brand": "Barissimo",
                "size": "32 fl oz",
            }
        ],
        retailers=["aldi"],
    )

    aldi = response.matches_by_retailer["aldi"]

    assert aldi.status == "no_match"
    assert aldi.best is None
    assert aldi.candidates[0].decision == "different"
