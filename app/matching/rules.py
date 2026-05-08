from typing import Final


STOPWORDS: Final[set[str]] = {
    "and",
    "brand",
    "fresh",
    "grocery",
    "of",
    "the",
    "with",
}

PHRASE_ALIASES: Final[tuple[tuple[str, str], ...]] = (
    ("2 percent", "2%"),
    ("two percent", "2%"),
    ("reduced fat", "2%"),
    ("1 percent", "1%"),
    ("one percent", "1%"),
    ("low fat", "1%"),
    ("fat free", "skim"),
    ("non fat", "nonfat"),
    ("lactose-free", "lactose free"),
    ("cage-free", "cage free"),
    ("free-range", "free range"),
    ("pasture-raised", "pasture raised"),
    ("extra-large", "extra large"),
    ("no-salt", "no salt"),
)

TOKEN_ALIASES: Final[dict[str, str]] = {
    "eggs": "egg",
    "loaves": "loaf",
    "slices": "sliced",
    "sticks": "stick",
    "quarters": "stick",
    "ounces": "oz",
    "ounce": "oz",
    "pounds": "lb",
    "pound": "lb",
    "lbs": "lb",
    "gallons": "gallon",
    "gal": "gallon",
    "quarts": "quart",
    "qt": "quart",
    "pints": "pint",
    "pt": "pint",
    "counts": "ct",
    "count": "ct",
    "packs": "pack",
    "pk": "pack",
}

CATEGORY_ALIASES: Final[dict[str, set[str]]] = {
    "milk": {"milk"},
    "eggs": {"egg"},
    "bread": {"bread", "loaf"},
    "butter": {"butter"},
    "cheese": {"cheese"},
    "packaged_good": {"cereal"},
}

STRICT_CATEGORIES: Final[set[str]] = {
    "milk",
    "eggs",
    "bread",
    "butter",
    "cheese",
}

CRITICAL_ATTRIBUTES: Final[dict[str, tuple[str, ...]]] = {
    "milk": ("fat_level", "organic", "lactose_free", "flavor"),
    "eggs": ("egg_size", "grade", "organic", "cage_free", "free_range", "pasture_raised"),
    "bread": ("bread_type", "organic"),
    "butter": ("salt", "form", "organic"),
    "cheese": ("variety", "form", "organic"),
}

SCORE_WEIGHTS: Final[dict[str, float]] = {
    "category": 0.20,
    "general_category": 0.12,
    "size_match": 0.25,
    "missing_size": 0.05,
    "attribute_match": 0.25,
    "attribute_missing": 0.12,
    "brand_match": 0.15,
    "brand_mismatch": 0.04,
    "token_similarity": 0.15,
}

SUBSTITUTE_THRESHOLD: Final[float] = 0.62
GENERAL_EQUIVALENCE_TOKEN_THRESHOLD: Final[float] = 0.72

REJECT_SCORES: Final[dict[str, float]] = {
    "size_conflict": 0.25,
    "attribute_conflict_cap": 0.45,
    "brand_conflict_cap": 0.55,
}

STORE_BRANDS: Final[dict[str, set[str]]] = {
    "walmart": {
        "bettergoods",
        "equate",
        "great value",
        "marketside",
        "sams choice",
    },
    "kroger": {
        "kroger",
        "private selection",
        "simple truth",
        "simple truth organic",
    },
    "publix": {
        "greenwise",
        "publix",
    },
    "aldi": {
        "countryside creamery",
        "fit active",
        "friendly farms",
        "happy farms",
        "livegfree",
        "millville",
        "simply nature",
        "specially selected",
    },
}

NATIONAL_BRANDS: Final[set[str]] = {
    "cabot",
    "cheerios",
    "daves killer bread",
    "egglands best",
    "fairlife",
    "horizon organic",
    "kraft",
    "lactaid",
    "land o lakes",
    "natures own",
    "pepperidge farm",
    "philadelphia",
    "sargento",
    "tillamook",
    "vital farms",
}

BRAND_ALIASES: Final[dict[str, str]] = {
    "great value brand": "great value",
    "kroger brand": "kroger",
    "publix brand": "publix",
    "sams choice brand": "sams choice",
    "simple truth organics": "simple truth organic",
}
