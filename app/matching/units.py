import re
from fractions import Fraction

from app.matching.models import ParsedSize


_VALUE_PATTERN = r"(?P<value>\d+(?:\.\d+)?|\d+\s*/\s*\d+)"
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
    r"counts?|ct\.?|"
    r"packs?|pk"
    r")"
)
_SIZE_RE = re.compile(rf"\b{_VALUE_PATTERN}\s*{_UNIT_PATTERN}\b", re.IGNORECASE)
_HALF_GALLON_RE = re.compile(r"\bhalf\s+(?:gallon|gal\.?)\b", re.IGNORECASE)
_DOZEN_RE = re.compile(r"\b(?:a\s+)?dozen\b", re.IGNORECASE)

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

_COUNT_UNITS = {
    "count",
    "counts",
    "ct",
    "ct.",
    "pack",
    "packs",
    "pk",
}


def _parse_number(value: str) -> float:
    compact = value.replace(" ", "")
    if "/" in compact:
        return float(Fraction(compact))
    return float(compact)


def _normalize_unit(unit: str) -> str:
    return re.sub(r"\s+", " ", unit.lower().strip())


def _size_from_match(match: re.Match, category: str | None = None) -> ParsedSize | None:
    value = _parse_number(match.group("value"))
    unit = _normalize_unit(match.group("unit"))
    source = match.group(0)

    if unit in _VOLUME_UNITS:
        return ParsedSize(value=value * _VOLUME_UNITS[unit], unit="fl_oz", source=source)

    if unit in _WEIGHT_UNITS:
        if unit in {"ounce", "ounces", "oz", "oz."} and category == "milk":
            return ParsedSize(value=value, unit="fl_oz", source=source)
        return ParsedSize(value=value * _WEIGHT_UNITS[unit], unit="oz", source=source)

    if unit in _COUNT_UNITS:
        return ParsedSize(value=value, unit="ct", source=source)

    return None


def parse_size(text: str | None, category: str | None = None) -> ParsedSize | None:
    if not text:
        return None

    if _HALF_GALLON_RE.search(text):
        return ParsedSize(value=64.0, unit="fl_oz", source="half gallon")

    if _DOZEN_RE.search(text):
        return ParsedSize(value=12.0, unit="ct", source="dozen")

    matches = [_size_from_match(match, category=category) for match in _SIZE_RE.finditer(text)]
    sizes = [size for size in matches if size is not None]
    if not sizes:
        return None

    if category == "eggs":
        count_sizes = [size for size in sizes if size.unit == "ct"]
        if count_sizes:
            return max(count_sizes, key=lambda size: size.value)

    measured_sizes = [size for size in sizes if size.unit != "ct"]
    if measured_sizes:
        return max(measured_sizes, key=lambda size: size.value)

    return max(sizes, key=lambda size: size.value)


def sizes_compatible(reference: ParsedSize, candidate: ParsedSize) -> bool:
    if reference.unit != candidate.unit:
        return False

    if reference.unit == "ct":
        return int(round(reference.value)) == int(round(candidate.value))

    tolerance = max(reference.value * 0.01, 0.05)
    return abs(reference.value - candidate.value) <= tolerance
