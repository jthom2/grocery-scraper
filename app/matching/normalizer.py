import re
from typing import Any

from app.matching.brands import classify_brand, infer_brand
from app.matching.models import ProductFingerprint
from app.matching.units import parse_size


_TOKEN_RE = re.compile(r"[a-z0-9%']+")
_STOPWORDS = {
    "and",
    "brand",
    "fresh",
    "grocery",
    "of",
    "the",
    "with",
}


def tokenize(text: str | None) -> list[str]:
    if not text:
        return []
    tokens = _TOKEN_RE.findall(text.lower().replace("&", " and "))
    return [token for token in tokens if token not in _STOPWORDS]


def detect_category(tokens: list[str]) -> str | None:
    token_set = set(tokens)

    if "milk" in token_set:
        return "milk"
    if "egg" in token_set or "eggs" in token_set:
        return "eggs"
    if "bread" in token_set or "loaf" in token_set:
        return "bread"
    if "butter" in token_set:
        return "butter"
    if "cheese" in token_set:
        return "cheese"

    return None


def _has_any(token_set: set[str], values: set[str]) -> bool:
    return bool(token_set & values)


def _phrase(text: str, value: str) -> bool:
    return value in text


def _milk_attributes(text: str, token_set: set[str]) -> dict[str, Any]:
    attrs = {
        "organic": "organic" in token_set,
        "lactose_free": _phrase(text, "lactose free"),
        "flavor": "plain",
    }

    if "chocolate" in token_set:
        attrs["flavor"] = "chocolate"
    elif "strawberry" in token_set:
        attrs["flavor"] = "strawberry"
    elif "vanilla" in token_set:
        attrs["flavor"] = "vanilla"

    if "2%" in token_set or _phrase(text, "2 percent") or _phrase(text, "reduced fat"):
        attrs["fat_level"] = "2%"
    elif "1%" in token_set or _phrase(text, "1 percent") or _phrase(text, "low fat"):
        attrs["fat_level"] = "1%"
    elif "skim" in token_set or _phrase(text, "fat free") or "nonfat" in token_set:
        attrs["fat_level"] = "skim"
    elif "whole" in token_set:
        attrs["fat_level"] = "whole"

    return attrs


def _egg_attributes(text: str, token_set: set[str]) -> dict[str, Any]:
    attrs = {
        "organic": "organic" in token_set,
        "cage_free": _phrase(text, "cage free"),
        "free_range": _phrase(text, "free range"),
        "pasture_raised": _phrase(text, "pasture raised"),
    }

    if _phrase(text, "extra large"):
        attrs["egg_size"] = "extra_large"
    elif "jumbo" in token_set:
        attrs["egg_size"] = "jumbo"
    elif "large" in token_set:
        attrs["egg_size"] = "large"
    elif "medium" in token_set:
        attrs["egg_size"] = "medium"
    elif "small" in token_set:
        attrs["egg_size"] = "small"

    if _phrase(text, "grade aa"):
        attrs["grade"] = "aa"
    elif _phrase(text, "grade a"):
        attrs["grade"] = "a"
    elif _phrase(text, "grade b"):
        attrs["grade"] = "b"

    return attrs


def _bread_attributes(text: str, token_set: set[str]) -> dict[str, Any]:
    attrs = {
        "organic": "organic" in token_set,
        "sliced": "sliced" in token_set,
    }

    if _phrase(text, "whole wheat"):
        attrs["bread_type"] = "whole_wheat"
    elif "wheat" in token_set:
        attrs["bread_type"] = "wheat"
    elif "white" in token_set:
        attrs["bread_type"] = "white"
    elif "sourdough" in token_set:
        attrs["bread_type"] = "sourdough"
    elif "rye" in token_set:
        attrs["bread_type"] = "rye"
    elif "brioche" in token_set:
        attrs["bread_type"] = "brioche"
    elif "multigrain" in token_set:
        attrs["bread_type"] = "multigrain"

    return attrs


def _butter_attributes(text: str, token_set: set[str]) -> dict[str, Any]:
    attrs = {
        "organic": "organic" in token_set,
    }

    if "unsalted" in token_set or _phrase(text, "no salt"):
        attrs["salt"] = "unsalted"
    elif "salted" in token_set:
        attrs["salt"] = "salted"

    if _has_any(token_set, {"sticks", "stick", "quarters"}):
        attrs["form"] = "sticks"
    elif _has_any(token_set, {"spread", "spreadable", "tub"}):
        attrs["form"] = "spread"

    return attrs


def _cheese_attributes(text: str, token_set: set[str]) -> dict[str, Any]:
    attrs = {
        "organic": "organic" in token_set,
    }

    for variety in (
        "cheddar",
        "mozzarella",
        "swiss",
        "provolone",
        "american",
        "parmesan",
        "colby",
        "monterey",
    ):
        if variety in token_set:
            attrs["variety"] = variety
            break

    if "shredded" in token_set:
        attrs["form"] = "shredded"
    elif "sliced" in token_set or "slices" in token_set:
        attrs["form"] = "sliced"
    elif "block" in token_set or "chunk" in token_set:
        attrs["form"] = "block"
    elif "string" in token_set:
        attrs["form"] = "string"
    elif "crumbles" in token_set or "crumbled" in token_set:
        attrs["form"] = "crumbled"

    return attrs


def extract_attributes(category: str | None, text: str, tokens: list[str]) -> dict[str, Any]:
    token_set = set(tokens)

    if category == "milk":
        return _milk_attributes(text, token_set)
    if category == "eggs":
        return _egg_attributes(text, token_set)
    if category == "bread":
        return _bread_attributes(text, token_set)
    if category == "butter":
        return _butter_attributes(text, token_set)
    if category == "cheese":
        return _cheese_attributes(text, token_set)

    return {}


def _combined_product_text(product: dict[str, Any]) -> str:
    parts = [
        product.get("name"),
        product.get("brand"),
        product.get("size"),
        product.get("unit_price"),
    ]
    return " ".join(str(part) for part in parts if part)


def _fingerprint(
    source_name: str,
    text: str,
    retailer: str | None = None,
    product_id: str | None = None,
    explicit_brand: str | None = None,
    is_query: bool = False,
) -> ProductFingerprint:
    tokens = tokenize(text)
    category = detect_category(tokens)
    normalized_brand = infer_brand(text, explicit_brand)
    brand_class = classify_brand(normalized_brand, retailer)
    size = parse_size(text, category=category)
    attributes = extract_attributes(category, text.lower(), tokens)

    return ProductFingerprint(
        source_name=source_name,
        retailer=retailer,
        product_id=product_id,
        brand=explicit_brand,
        normalized_brand=normalized_brand,
        brand_class=brand_class,
        category=category,
        tokens=tokens,
        size=size,
        attributes=attributes,
        is_query=is_query,
    )


def fingerprint_query(query: str) -> ProductFingerprint:
    return _fingerprint(
        source_name=query,
        text=query,
        is_query=True,
    )


def fingerprint_product(product: dict[str, Any]) -> ProductFingerprint:
    text = _combined_product_text(product)
    return _fingerprint(
        source_name=str(product.get("name") or text),
        text=text,
        retailer=product.get("retailer"),
        product_id=product.get("product_id"),
        explicit_brand=product.get("brand"),
        is_query=False,
    )
