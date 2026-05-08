import re
from fractions import Fraction

from app.matching.models import ParsedSize


_NUMBER_PATTERN = r"\d+\s+\d+\s*/\s*\d+|\d+\s*/\s*\d+|\d+(?:\.\d+)?"
_VALUE_PATTERN = rf"(?P<value>{_NUMBER_PATTERN})"
_UNIT_PATTERN = (
    r"(?P<unit>"
    r"fluid\s+ounces?|fl\.?\s*oz\.?|floz|"
    r"gallons?|gal\.?|"
    r"quarts?|qt\.?|"
    r"pints?|pt\.?|"
    r"pounds?|lbs?\.?|lb\.?|"
    r"ounces?|oz\.?|"
    r"grams?|g|"
    r"kilograms?|kg|"
    r"liters?|litres?|lt\.?|"
    r"milliliters?|millilitres?|ml|"
    r"counts?|ct\.?|"
    r"packs?|pk|"
    r"square\s+feet|sq\s*\.?\s*ft\.?|"
    r"(?:ea\.?|each)"
    r")"
)
_SIZE_RE = re.compile(rf"\b{_VALUE_PATTERN}\s*{_UNIT_PATTERN}\b", re.IGNORECASE)
_MULTIPACK_RE = re.compile(
    rf"\b(?P<count>\d+)\s*(?:x|×|pk|packs?(?:\s+of)?|-\s*packs?)\s*"
    rf"(?P<item_value>{_NUMBER_PATTERN})\s*"
    rf"(?P<item_unit>"
    r"fluid\s+ounces?|fl\.?\s*oz\.?|floz|"
    r"gallons?|gal\.?|"
    r"quarts?|qt\.?|"
    r"pints?|pt\.?|"
    r"pounds?|lbs?\.?|lb\.?|"
    r"ounces?|oz\.?|"
    r"grams?|g|"
    r"kilograms?|kg|"
    r"liters?|litres?|lt\.?|"
    r"milliliters?|millilitres?|ml|"
    r"counts?|ct\.?|"
    r"square\s+feet|sq\s*\.?\s*ft\.?"
    r")\b",
    re.IGNORECASE,
)
# comma-separated multipack (e.g. "6 pk, 16.9 fl oz")
_COMMA_MULTIPACK_RE = re.compile(
    rf"\b(?P<count>\d+)\s*(?:pk|pack)\s*,\s*"
    rf"(?P<item_value>{_NUMBER_PATTERN})\s*"
    rf"(?P<item_unit>"
    r"fluid\s+ounces?|fl\.?\s*oz\.?|floz|"
    r"gallons?|gal\.?|"
    r"quarts?|qt\.?|"
    r"pints?|pt\.?|"
    r"pounds?|lbs?\.?|lb\.?|"
    r"ounces?|oz\.?|"
    r"grams?|g|"
    r"kilograms?|kg|"
    r"liters?|litres?|lt\.?|"
    r"milliliters?|millilitres?|ml"
    r")\b",
    re.IGNORECASE,
)
# "twin pack N unit" / "double pack N unit"
_TWIN_PACK_RE = re.compile(
    rf"\b(?P<count>twin|double|triple)\s+packs?\s+"
    rf"(?P<item_value>{_NUMBER_PATTERN})\s*"
    rf"(?P<item_unit>"
    r"fluid\s+ounces?|fl\.?\s*oz\.?|floz|"
    r"gallons?|gal\.?|"
    r"ounces?|oz\.?|"
    r"pounds?|lbs?\.?|lb\.?"
    r")\b",
    re.IGNORECASE,
)
_TWIN_PACK_COUNTS = {"twin": 2, "double": 2, "triple": 3}

_HALF_GALLON_RE = re.compile(r"\bhalf\s+(?:gallon|gal\.?)\b", re.IGNORECASE)
_BARE_GALLON_RE = re.compile(r"\b(?:gallons?|gal\.?)\b", re.IGNORECASE)
_DOZEN_RE = re.compile(r"\b(?:a\s+)?dozen\b", re.IGNORECASE)
_TOTAL_WEIGHT_RE = re.compile(
    rf"\b(?:total\s+(?:weight|wt\.?)|net\s+wt\.?)\s*:?\s*"
    rf"(?P<value>{_NUMBER_PATTERN})\s*"
    rf"(?P<unit>"
    r"fluid\s+ounces?|fl\.?\s*oz\.?|floz|"
    r"ounces?|oz\.?|"
    r"pounds?|lbs?\.?|lb\.?|"
    r"grams?|g|"
    r"kilograms?|kg"
    r")\b",
    re.IGNORECASE,
)

_VOLUME_UNITS = {
    "gallon": 128.0,
    "gallons": 128.0,
    "gal": 128.0,
    "gal.": 128.0,
    "quart": 32.0,
    "quarts": 32.0,
    "qt": 32.0,
    "qt.": 32.0,
    "pint": 16.0,
    "pints": 16.0,
    "pt": 16.0,
    "pt.": 16.0,
    "fluid ounce": 1.0,
    "fluid ounces": 1.0,
    "fl oz": 1.0,
    "fl. oz": 1.0,
    "fl. oz.": 1.0,
    "floz": 1.0,
}

_WEIGHT_UNITS = {
    "pound": 16.0,
    "pounds": 16.0,
    "lb": 16.0,
    "lb.": 16.0,
    "lbs": 16.0,
    "lbs.": 16.0,
    "ounce": 1.0,
    "ounces": 1.0,
    "oz": 1.0,
    "oz.": 1.0,
    "gram": 1 / 28.349523125,
    "grams": 1 / 28.349523125,
    "g": 1 / 28.349523125,
    "kilogram": 1000 / 28.349523125,
    "kilograms": 1000 / 28.349523125,
    "kg": 1000 / 28.349523125,
}

_METRIC_VOLUME_UNITS = {
    "milliliter": 1.0,
    "milliliters": 1.0,
    "millilitre": 1.0,
    "millilitres": 1.0,
    "ml": 1.0,
    "liter": 1000.0,
    "liters": 1000.0,
    "litre": 1000.0,
    "litres": 1000.0,
    "lt": 1000.0,
    "lt.": 1000.0,
}

_COUNT_UNITS = {
    "count",
    "counts",
    "ct",
    "ct.",
    "pack",
    "packs",
    "pk",
}

_EACH_UNITS = {"ea", "ea.", "each"}

_AREA_UNITS = {
    "sq ft": 1.0,
    "sq. ft": 1.0,
    "sq. ft.": 1.0,
    "sq ft.": 1.0,
    "square feet": 1.0,
}

# categories where "per each" / single-item is the natural unit
_EACH_CATEGORIES = {"produce"}

# categories that prefer sq_ft over ct
_AREA_CATEGORIES = {"paper_goods"}

# categories that prefer count over measured size
_COUNT_PREFERRED_CATEGORIES = {"eggs"}

# categories that prefer weight
_WEIGHT_PREFERRED_CATEGORIES = {"chicken", "beef", "pork"}


def _parse_number(value: str) -> float:
    stripped = re.sub(r"\s+", " ", value.strip())
    if " " in stripped and "/" in stripped:
        whole, fraction = stripped.split(" ", 1)
        return float(whole) + float(Fraction(fraction.replace(" ", "")))

    compact = value.replace(" ", "")
    if "/" in compact:
        return float(Fraction(compact))
    return float(compact)


def _normalize_unit(unit: str) -> str:
    return re.sub(r"\s+", " ", unit.lower().strip())


def _size_from_parts(value: float, unit: str, source: str, category: str | None = None) -> ParsedSize | None:
    if unit in _VOLUME_UNITS:
        return ParsedSize(value=value * _VOLUME_UNITS[unit], unit="fl_oz", source=source)

    if unit in _METRIC_VOLUME_UNITS:
        return ParsedSize(value=value * _METRIC_VOLUME_UNITS[unit], unit="ml", source=source)

    if unit in _WEIGHT_UNITS:
        if unit in {"ounce", "ounces", "oz", "oz."} and category == "milk":
            return ParsedSize(value=value, unit="fl_oz", source=source)
        return ParsedSize(value=value * _WEIGHT_UNITS[unit], unit="oz", source=source)

    if unit in _AREA_UNITS:
        return ParsedSize(value=value * _AREA_UNITS[unit], unit="sq_ft", source=source)

    if unit in _EACH_UNITS:
        return ParsedSize(value=value, unit="each", source=source)

    if unit in _COUNT_UNITS:
        return ParsedSize(value=value, unit="ct", source=source)

    return None


def _size_from_match(match: re.Match, category: str | None = None) -> ParsedSize | None:
    value = _parse_number(match.group("value"))
    unit = _normalize_unit(match.group("unit"))
    source = match.group(0)
    return _size_from_parts(value, unit, source, category=category)


def _size_from_multipack(match: re.Match, category: str | None = None) -> ParsedSize | None:
    count = _parse_number(match.group("count"))
    value = _parse_number(match.group("item_value"))
    unit = _normalize_unit(match.group("item_unit"))
    source = match.group(0)
    return _size_from_parts(count * value, unit, source, category=category)


def _size_from_twin_pack(match: re.Match, category: str | None = None) -> ParsedSize | None:
    count_word = match.group("count").lower()
    count = _TWIN_PACK_COUNTS.get(count_word, 2)
    value = _parse_number(match.group("item_value"))
    unit = _normalize_unit(match.group("item_unit"))
    source = match.group(0)
    return _size_from_parts(count * value, unit, source, category=category)


def parse_size(text: str | None, category: str | None = None) -> ParsedSize | None:
    if not text:
        return None

    # total / net weight overrides everything when present
    total_match = _TOTAL_WEIGHT_RE.search(text)
    if total_match:
        value = _parse_number(total_match.group("value"))
        unit = _normalize_unit(total_match.group("unit"))
        source = total_match.group(0)
        result = _size_from_parts(value, unit, source, category=category)
        if result:
            return result

    if _HALF_GALLON_RE.search(text):
        return ParsedSize(value=64.0, unit="fl_oz", source="half gallon")

    if _DOZEN_RE.search(text):
        return ParsedSize(value=12.0, unit="ct", source="dozen")

    if category == "milk" and not _SIZE_RE.search(text) and _BARE_GALLON_RE.search(text):
        return ParsedSize(value=128.0, unit="fl_oz", source="gallon")

    # gather all size candidates
    multipack_sizes = [_size_from_multipack(m, category=category) for m in _MULTIPACK_RE.finditer(text)]
    comma_sizes = [_size_from_multipack(m, category=category) for m in _COMMA_MULTIPACK_RE.finditer(text)]
    twin_sizes = [_size_from_twin_pack(m, category=category) for m in _TWIN_PACK_RE.finditer(text)]
    match_sizes = [_size_from_match(m, category=category) for m in _SIZE_RE.finditer(text)]

    sizes = [s for s in [*multipack_sizes, *comma_sizes, *twin_sizes, *match_sizes] if s is not None]
    if not sizes:
        return None

    # category-aware preference
    if category in _COUNT_PREFERRED_CATEGORIES:
        count_sizes = [s for s in sizes if s.unit == "ct"]
        if count_sizes:
            return max(count_sizes, key=lambda s: s.value)

    if category in _AREA_CATEGORIES:
        area_sizes = [s for s in sizes if s.unit == "sq_ft"]
        if area_sizes:
            return max(area_sizes, key=lambda s: s.value)

    if category in _EACH_CATEGORIES:
        each_sizes = [s for s in sizes if s.unit == "each"]
        if each_sizes:
            return max(each_sizes, key=lambda s: s.value)

    if category in _WEIGHT_PREFERRED_CATEGORIES:
        weight_sizes = [s for s in sizes if s.unit == "oz"]
        if weight_sizes:
            return max(weight_sizes, key=lambda s: s.value)

    # default: prefer measured over count
    measured_sizes = [s for s in sizes if s.unit not in {"ct", "each"}]
    if measured_sizes:
        return max(measured_sizes, key=lambda s: s.value)

    return max(sizes, key=lambda s: s.value)


# fl_oz -> ml conversion factor
_FL_OZ_TO_ML = 29.5735


def sizes_compatible(reference: ParsedSize, candidate: ParsedSize) -> bool:
    # cross-unit volume: fl_oz <-> ml
    if {reference.unit, candidate.unit} == {"fl_oz", "ml"}:
        ref_ml = reference.value * _FL_OZ_TO_ML if reference.unit == "fl_oz" else reference.value
        cand_ml = candidate.value * _FL_OZ_TO_ML if candidate.unit == "fl_oz" else candidate.value
        tolerance = max(ref_ml * 0.02, 1.0)
        return abs(ref_ml - cand_ml) <= tolerance

    if reference.unit != candidate.unit:
        return False

    if reference.unit in {"ct", "each"}:
        return int(round(reference.value)) == int(round(candidate.value))

    tolerance = max(reference.value * 0.01, 0.05)
    return abs(reference.value - candidate.value) <= tolerance
