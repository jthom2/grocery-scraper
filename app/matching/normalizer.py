import re
from typing import Any

from app.matching.brands import classify_brand, infer_brand
from app.matching.models import ProductFingerprint
from app.matching.rules import CATEGORY_ALIASES, PHRASE_ALIASES, STOPWORDS, TOKEN_ALIASES
from app.matching.units import parse_size


_TOKEN_RE = re.compile(r"[a-z0-9%']+")


def normalize_text(text: str | None) -> str:
    if not text:
        return ""

    value = text.lower().replace("&", " and ")
    for source, replacement in PHRASE_ALIASES:
        pattern = rf"(?<![a-z0-9]){re.escape(source)}(?![a-z0-9])"
        value = re.sub(pattern, replacement, value)
    return value


def tokenize(text: str | None) -> list[str]:
    normalized = normalize_text(text)
    tokens = []
    for token in _TOKEN_RE.findall(normalized):
        canonical = TOKEN_ALIASES.get(token.replace("'", ""), token.replace("'", ""))
        if canonical not in STOPWORDS:
            tokens.append(canonical)
    return tokens


# categories that should be checked before produce (which has broad triggers)
_CATEGORY_PRIORITY = [
    "milk", "eggs", "bread", "butter", "cheese",
    "yogurt", "juice", "coffee",
    "pasta", "rice",
    "chicken", "beef", "pork",
    "snacks", "water", "paper_goods", "packaged_good",
    "produce",
    "frozen",
]

# phrase-based categories that require multi-word matching
_PHRASE_CATEGORIES: dict[str, list[str]] = {
    "paper_goods": ["paper towel", "toilet paper"],
}


def detect_category(tokens: list[str]) -> str | None:
    token_set = set(tokens)
    joined = " ".join(tokens)

    has_frozen = "frozen" in token_set
    non_frozen_tokens = token_set - {"frozen"}

    for category in _CATEGORY_PRIORITY:
        if category == "frozen":
            continue

        # check phrase-based matches first
        phrases = _PHRASE_CATEGORIES.get(category, [])
        for phrase in phrases:
            if phrase in joined:
                if has_frozen:
                    return "frozen"
                return category

        # then token-based
        aliases = CATEGORY_ALIASES.get(category, set())
        if non_frozen_tokens & aliases:
            if has_frozen:
                return "frozen"
            return category

    if has_frozen:
        return "frozen"

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

    if _has_any(token_set, {"stick", "quarters"}):
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
    elif "sliced" in token_set:
        attrs["form"] = "sliced"
    elif "block" in token_set or "chunk" in token_set:
        attrs["form"] = "block"
    elif "string" in token_set:
        attrs["form"] = "string"
    elif "crumbles" in token_set or "crumbled" in token_set:
        attrs["form"] = "crumbled"

    return attrs


def _yogurt_attributes(text: str, token_set: set[str]) -> dict[str, Any]:
    attrs = {
        "organic": "organic" in token_set,
    }

    if "greek" in token_set:
        attrs["style"] = "greek"
    elif "icelandic" in token_set or "skyr" in token_set:
        attrs["style"] = "icelandic"
    else:
        attrs["style"] = "regular"

    # flavor detection
    for flavor in ("vanilla", "strawberry", "blueberry", "peach",
                   "raspberry", "cherry", "mango", "coconut",
                   "honey", "lemon", "lime", "key lime"):
        if flavor in token_set or _phrase(text, flavor):
            attrs["flavor"] = flavor
            break
    else:
        if "plain" in token_set or "original" in token_set:
            attrs["flavor"] = "plain"

    # fat level
    if "nonfat" in token_set or "skim" in token_set or _phrase(text, "fat free") or "0%" in token_set:
        attrs["fat_level"] = "nonfat"
    elif "2%" in token_set or _phrase(text, "low fat"):
        attrs["fat_level"] = "lowfat"
    elif "whole" in token_set or _phrase(text, "whole milk"):
        attrs["fat_level"] = "whole"

    return attrs


def _juice_attributes(text: str, token_set: set[str]) -> dict[str, Any]:
    attrs = {
        "organic": "organic" in token_set,
    }

    # fruit detection
    for fruit in ("orange", "apple", "grape", "cranberry", "pineapple",
                  "grapefruit", "lemon", "lemonade", "tomato", "carrot"):
        if fruit in token_set:
            attrs["fruit"] = fruit
            break

    if _phrase(text, "not from concentrate"):
        attrs["concentrate"] = "not_from_concentrate"
    elif _phrase(text, "from concentrate"):
        attrs["concentrate"] = "from_concentrate"

    return attrs


def _coffee_attributes(text: str, token_set: set[str]) -> dict[str, Any]:
    attrs = {
        "organic": "organic" in token_set,
        "decaf": _has_any(token_set, {"decaf", "decaffeinated"}),
    }

    if "dark" in token_set:
        attrs["roast"] = "dark"
    elif "medium" in token_set:
        attrs["roast"] = "medium"
    elif "light" in token_set or "blonde" in token_set:
        attrs["roast"] = "light"

    if _phrase(text, "whole bean") or _has_any(token_set, {"bean", "beans"}):
        attrs["form"] = "whole_bean"
    elif _has_any(token_set, {"ground"}):
        attrs["form"] = "ground"
    elif _has_any(token_set, {"pods", "pod", "kcup", "capsule", "capsules"}):
        attrs["form"] = "pods"
    elif "instant" in token_set:
        attrs["form"] = "instant"

    return attrs


def _chicken_attributes(text: str, token_set: set[str]) -> dict[str, Any]:
    attrs = {
        "organic": "organic" in token_set,
        "boneless": "boneless" in token_set,
        "skinless": "skinless" in token_set,
    }

    for cut in ("breast", "thigh", "drumstick", "wing", "tenderloin", "whole"):
        if cut in token_set:
            attrs["cut"] = cut
            break

    if "frozen" in token_set or _phrase(text, "flash frozen"):
        attrs["fresh_or_frozen"] = "frozen"
    else:
        attrs["fresh_or_frozen"] = "fresh"

    return attrs


def _beef_attributes(text: str, token_set: set[str]) -> dict[str, Any]:
    attrs = {
        "organic": "organic" in token_set,
        "grass_fed": _phrase(text, "grass fed"),
    }

    if "ground" in token_set:
        attrs["cut"] = "ground"
    elif "steak" in token_set:
        attrs["cut"] = "steak"
    elif "roast" in token_set:
        attrs["cut"] = "roast"
    elif "stew" in token_set:
        attrs["cut"] = "stew"
    elif "tenderloin" in token_set:
        attrs["cut"] = "tenderloin"
    elif "brisket" in token_set:
        attrs["cut"] = "brisket"

    # lean percentage (e.g. "80/20", "93/7", "90% lean")
    lean_match = re.search(r"(\d{2,3})\s*/\s*(\d{1,2})", text)
    if lean_match:
        attrs["lean_pct"] = int(lean_match.group(1))
    else:
        lean_pct_match = re.search(r"(\d{2,3})\s*%\s*lean", text)
        if lean_pct_match:
            attrs["lean_pct"] = int(lean_pct_match.group(1))

    return attrs


def _pork_attributes(text: str, token_set: set[str]) -> dict[str, Any]:
    attrs = {
        "organic": "organic" in token_set,
    }

    for cut in ("chop", "tenderloin", "roast", "ribs", "loin",
                "shoulder", "ground", "bacon", "ham", "sausage"):
        if cut in token_set:
            attrs["cut"] = cut
            break

    if "frozen" in token_set:
        attrs["fresh_or_frozen"] = "frozen"
    else:
        attrs["fresh_or_frozen"] = "fresh"

    return attrs


def _produce_attributes(text: str, token_set: set[str]) -> dict[str, Any]:
    return {
        "organic": "organic" in token_set,
    }


def _pasta_attributes(text: str, token_set: set[str]) -> dict[str, Any]:
    attrs = {
        "organic": "organic" in token_set,
        "whole_wheat": _phrase(text, "whole wheat") or "whole" in token_set,
    }

    for shape in ("spaghetti", "penne", "linguine", "fettuccine",
                   "rigatoni", "rotini", "elbow", "macaroni",
                   "lasagna", "farfalle", "angel hair", "ziti"):
        if shape in token_set or _phrase(text, shape):
            attrs["shape"] = shape
            break

    return attrs


def _rice_attributes(text: str, token_set: set[str]) -> dict[str, Any]:
    attrs = {
        "organic": "organic" in token_set,
    }

    if "jasmine" in token_set:
        attrs["variety"] = "jasmine"
    elif "basmati" in token_set:
        attrs["variety"] = "basmati"
    elif "wild" in token_set:
        attrs["variety"] = "wild"
    elif "brown" in token_set:
        attrs["variety"] = "brown"
    elif "white" in token_set:
        attrs["variety"] = "white"
    elif "arborio" in token_set:
        attrs["variety"] = "arborio"

    return attrs


def _frozen_attributes(text: str, token_set: set[str]) -> dict[str, Any]:
    return {
        "organic": "organic" in token_set,
        "frozen": True,
    }


def _paper_goods_attributes(text: str, token_set: set[str]) -> dict[str, Any]:
    attrs: dict[str, Any] = {}

    if _phrase(text, "paper towel"):
        attrs["type"] = "paper_towel"
    elif _phrase(text, "toilet paper") or "bath" in token_set:
        attrs["type"] = "toilet_paper"
    elif "napkin" in token_set:
        attrs["type"] = "napkin"
    elif "tissue" in token_set:
        attrs["type"] = "tissue"

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
    if category == "yogurt":
        return _yogurt_attributes(text, token_set)
    if category == "juice":
        return _juice_attributes(text, token_set)
    if category == "coffee":
        return _coffee_attributes(text, token_set)
    if category == "chicken":
        return _chicken_attributes(text, token_set)
    if category == "beef":
        return _beef_attributes(text, token_set)
    if category == "pork":
        return _pork_attributes(text, token_set)
    if category == "produce":
        return _produce_attributes(text, token_set)
    if category == "pasta":
        return _pasta_attributes(text, token_set)
    if category == "rice":
        return _rice_attributes(text, token_set)
    if category == "frozen":
        return _frozen_attributes(text, token_set)
    if category == "paper_goods":
        return _paper_goods_attributes(text, token_set)

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
    normalized_text = normalize_text(text)
    tokens = tokenize(text)
    category = detect_category(tokens)
    normalized_brand = infer_brand(text, explicit_brand)
    brand_class = classify_brand(normalized_brand, retailer)
    size = parse_size(text, category=category)
    attributes = extract_attributes(category, normalized_text, tokens)

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
