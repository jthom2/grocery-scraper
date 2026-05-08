import re

from app.matching.rules import BRAND_ALIASES, NATIONAL_BRANDS, STORE_BRANDS


_ALL_STORE_BRANDS = {brand for brands in STORE_BRANDS.values() for brand in brands}


def normalize_brand(brand: str | None) -> str | None:
    if not brand:
        return None
    value = brand.lower().replace("&", " and ").replace("'", "")
    value = re.sub(r"[^a-z0-9%']+", " ", value)
    value = re.sub(r"\s+", " ", value).strip()
    value = BRAND_ALIASES.get(value, value)
    return value or None


def infer_brand(name: str | None, explicit_brand: str | None = None) -> str | None:
    normalized = normalize_brand(explicit_brand)
    if normalized:
        return normalized

    source = normalize_brand(name)
    if not source:
        return None

    for brand in sorted(_ALL_STORE_BRANDS, key=len, reverse=True):
        if source == brand or source.startswith(f"{brand} "):
            return brand

    for brand in sorted(NATIONAL_BRANDS, key=len, reverse=True):
        if source == brand or source.startswith(f"{brand} "):
            return brand

    return None


def classify_brand(brand: str | None, retailer: str | None = None) -> str:
    normalized = normalize_brand(brand)
    if not normalized:
        return "unknown"

    retailer_key = retailer.lower() if retailer else None
    if retailer_key and normalized in STORE_BRANDS.get(retailer_key, set()):
        return "store_brand"

    if normalized in _ALL_STORE_BRANDS:
        return "store_brand"

    return "national_brand"


def brand_allows_equivalence(reference, candidate) -> tuple[bool, str]:
    if reference.is_query and reference.brand_class == "unknown":
        return True, "generic query allows brand-neutral equivalence"

    if reference.normalized_brand and reference.normalized_brand == candidate.normalized_brand:
        return True, f"same brand: {reference.normalized_brand}"

    if reference.brand_class == "store_brand" and candidate.brand_class == "store_brand":
        return True, "store-brand equivalence allowed"

    if reference.brand_class == "national_brand" or candidate.brand_class == "national_brand":
        return False, "national brands require the same brand"

    return False, "unknown brands are not equivalent"
