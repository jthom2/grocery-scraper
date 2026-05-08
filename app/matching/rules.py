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
    ("fat-free", "skim"),
    ("fat free", "skim"),
    ("non-fat", "nonfat"),
    ("non fat", "nonfat"),
    ("lactose-free", "lactose free"),
    ("cage-free", "cage free"),
    ("free-range", "free range"),
    ("pasture-raised", "pasture raised"),
    ("extra-large", "extra large"),
    ("no-salt", "no salt"),
    # meat / poultry
    ("grass-fed", "grass fed"),
    ("bone-in", "bone in"),
    ("skin-on", "skin on"),
    # juice
    ("not from concentrate", "not from concentrate"),
    ("from concentrate", "from concentrate"),
    # coffee
    ("whole-bean", "whole bean"),
    ("cold-brew", "cold brew"),
    # frozen
    ("flash-frozen", "flash frozen"),
    # paper goods
    ("paper towels", "paper towel"),
    ("toilet paper", "toilet paper"),
    # produce
    ("sweet potato", "sweet potato"),
    # general hyphenated compound phrases
    ("multi-grain", "multigrain"),
    ("whole-wheat", "whole wheat"),
)

TOKEN_ALIASES: Final[dict[str, str]] = {
    # existing
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
    # produce plurals
    "bananas": "banana",
    "apples": "apple",
    "avocados": "avocado",
    "tomatoes": "tomato",
    "onions": "onion",
    "potatoes": "potato",
    "lemons": "lemon",
    "limes": "lime",
    "oranges": "orange",
    "peppers": "pepper",
    "cucumbers": "cucumber",
    "carrots": "carrot",
    "strawberries": "strawberry",
    "blueberries": "blueberry",
    "grapes": "grape",
    # meat / poultry
    "chickens": "chicken",
    "breasts": "breast",
    "thighs": "thigh",
    "drumsticks": "drumstick",
    "wings": "wing",
    "tenderloins": "tenderloin",
    "steaks": "steak",
    "roasts": "roast",
    # dairy
    "yogurts": "yogurt",
    "yoghurt": "yogurt",
    "yoghurts": "yogurt",
    # metric
    "liters": "liter",
    "litres": "liter",
    "litre": "liter",
    "milliliters": "ml",
    "millilitres": "ml",
    "milliliter": "ml",
    "millilitre": "ml",
    # paper / household
    "rolls": "roll",
    "sheets": "sheet",
    "towels": "towel",
    # pasta shapes
    "spaghettis": "spaghetti",
    "pennes": "penne",
    "rigatonis": "rigatoni",
    "rotinis": "rotini",
    "elbows": "elbow",
}

CATEGORY_ALIASES: Final[dict[str, set[str]]] = {
    "milk": {"milk"},
    "eggs": {"egg"},
    "bread": {"bread", "loaf"},
    "butter": {"butter"},
    "cheese": {"cheese"},
    "yogurt": {"yogurt"},
    "juice": {"juice"},
    "coffee": {"coffee"},
    "pasta": {"pasta", "spaghetti", "penne", "linguine", "fettuccine",
              "macaroni", "rigatoni", "rotini", "elbow", "lasagna"},
    "rice": {"rice"},
    "chicken": {"chicken"},
    "beef": {"beef"},
    "pork": {"pork"},
    "produce": {"banana", "apple", "avocado", "tomato", "onion",
                "potato", "lettuce", "lemon", "lime", "orange",
                "pepper", "cucumber", "carrot", "strawberry",
                "blueberry", "grape", "celery", "broccoli",
                "spinach", "kale", "sweet potato"},
    "frozen": {"frozen"},
    "water": {"water"},
    "snacks": {"chips", "crackers", "pretzels", "popcorn", "snack"},
    "paper_goods": {"paper towel", "toilet paper", "napkin", "tissue"},
    "packaged_good": {"cereal"},
}

STRICT_CATEGORIES: Final[set[str]] = {
    "milk",
    "eggs",
    "bread",
    "butter",
    "cheese",
    "yogurt",
    "juice",
    "coffee",
    "chicken",
    "beef",
    "pork",
    "produce",
    "pasta",
    "rice",
}

CRITICAL_ATTRIBUTES: Final[dict[str, tuple[str, ...]]] = {
    "milk": ("fat_level", "organic", "lactose_free", "flavor", "form"),
    "eggs": ("egg_size", "grade", "organic", "cage_free", "free_range", "pasture_raised"),
    "bread": ("bread_type", "organic"),
    "butter": ("salt", "form", "organic"),
    "cheese": ("variety", "form", "organic"),
    "yogurt": ("style", "flavor", "fat_level", "organic"),
    "juice": ("fruit", "concentrate", "organic"),
    "coffee": ("roast", "form", "decaf", "organic"),
    "chicken": ("cut", "fresh_or_frozen", "boneless", "skinless", "organic"),
    "beef": ("cut", "lean_pct", "organic", "grass_fed"),
    "pork": ("cut", "fresh_or_frozen", "organic"),
    "produce": ("organic",),
    "pasta": ("shape", "organic", "whole_wheat"),
    "rice": ("variety", "organic"),
}

SUBSTITUTE_THRESHOLD: Final[float] = 0.62
GENERAL_EQUIVALENCE_TOKEN_THRESHOLD: Final[float] = 0.72

REJECT_SCORES: Final[dict[str, float]] = {
    "size_conflict": 0.25,
    "attribute_conflict_cap": 0.45,
    "brand_conflict_cap": 0.55,
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

STORE_BRANDS: Final[dict[str, set[str]]] = {
    "walmart": {
        "bettergoods",
        "equate",
        "great value",
        "marketside",
        "parents choice",
        "sams choice",
    },
    "kroger": {
        "comforts",
        "heritage farm",
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
        "bakers corner",
        "brookdale",
        "clancys",
        "countryside creamery",
        "fit active",
        "friendly farms",
        "goldhen",
        "happy farms",
        "kirkwood",
        "little salad bar",
        "livegfree",
        "millville",
        "natures nectar",
        "simply nature",
        "specially selected",
    },
}

NATIONAL_BRANDS: Final[set[str]] = {
    # dairy / eggs
    "cabot",
    "chobani",
    "dannon",
    "egglands best",
    "fage",
    "fairlife",
    "horizon organic",
    "lactaid",
    "land o lakes",
    "tillamook",
    "vital farms",
    "yoplait",
    # cheese
    "kraft",
    "philadelphia",
    "sargento",
    # bread
    "daves killer bread",
    "natures own",
    "pepperidge farm",
    # cereal
    "cheerios",
    # juice
    "minute maid",
    "simply",
    "tropicana",
    # coffee
    "dunkin",
    "folgers",
    "maxwell house",
    "starbucks",
    # pasta
    "barilla",
    "de cecco",
    "ronzoni",
    # rice
    "lundberg",
    "minute rice",
    "uncle bens",
    # chicken / meat
    "perdue",
    "tyson",
    # snacks
    "cheez it",
    "doritos",
    "goldfish",
    "lays",
    # paper goods
    "bounty",
    "charmin",
    "scott",
    "viva",
}

BRAND_ALIASES: Final[dict[str, str]] = {
    "great value brand": "great value",
    "kroger brand": "kroger",
    "publix brand": "publix",
    "sams choice brand": "sams choice",
    "simple truth organics": "simple truth organic",
    "cheez-it": "cheez it",
    "cheez-its": "cheez it",
}
