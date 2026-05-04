from typing import Any

from app.matching.brands import brand_allows_equivalence
from app.matching.models import MatchResult, ProductFingerprint
from app.matching.units import sizes_compatible


_CRITICAL_ATTRIBUTES = {
    "milk": ("fat_level", "organic", "lactose_free", "flavor"),
    "eggs": ("egg_size", "grade", "organic", "cage_free", "free_range", "pasture_raised"),
    "bread": ("bread_type", "organic"),
    "butter": ("salt", "form", "organic"),
    "cheese": ("variety", "form", "organic"),
}


def _token_similarity(reference: ProductFingerprint, candidate: ProductFingerprint) -> float:
    left = set(reference.tokens)
    right = set(candidate.tokens)
    if not left or not right:
        return 0.0
    return len(left & right) / len(left | right)


def _critical_attribute_result(reference: ProductFingerprint, candidate: ProductFingerprint) -> tuple[bool, bool, list[str], list[str]]:
    reasons = []
    penalties = []
    has_missing = False

    for attr in _CRITICAL_ATTRIBUTES.get(reference.category or "", ()):
        ref_value = reference.attributes.get(attr)
        candidate_value = candidate.attributes.get(attr)

        if ref_value is None and candidate_value is None:
            continue

        if ref_value is None or candidate_value is None:
            if ref_value not in (None, False) or candidate_value not in (None, False):
                has_missing = True
                penalties.append(f"missing critical attribute: {attr}")
            continue

        if ref_value != candidate_value:
            penalties.append(f"critical attribute conflict: {attr} ({ref_value} vs {candidate_value})")
            return False, has_missing, reasons, penalties

        if ref_value not in (None, False):
            reasons.append(f"same {attr}: {ref_value}")

    return True, has_missing, reasons, penalties


def _same_category(reference: ProductFingerprint, candidate: ProductFingerprint) -> bool:
    return bool(reference.category and candidate.category and reference.category == candidate.category)


def score_fingerprints(
    reference: ProductFingerprint,
    candidate: ProductFingerprint,
    product: dict[str, Any] | None = None,
    equivalence_threshold: float = 0.82,
) -> MatchResult:
    reasons = []
    penalties = []
    score = 0.0
    equivalent_possible = True

    if not _same_category(reference, candidate):
        penalties.append(f"category mismatch: {reference.category or 'unknown'} vs {candidate.category or 'unknown'}")
        return MatchResult(
            decision="different",
            score=0.0,
            fingerprint=candidate,
            product=product,
            reasons=reasons,
            penalties=penalties,
        )

    score += 0.2
    reasons.append(f"same category: {reference.category}")

    if reference.size and candidate.size:
        if not sizes_compatible(reference.size, candidate.size):
            penalties.append(
                f"size conflict: {reference.size.value:g} {reference.size.unit} vs "
                f"{candidate.size.value:g} {candidate.size.unit}"
            )
            return MatchResult(
                decision="different",
                score=0.25,
                fingerprint=candidate,
                product=product,
                reasons=reasons,
                penalties=penalties,
            )
        score += 0.25
        reasons.append(f"same normalized size: {reference.size.value:g} {reference.size.unit}")
    else:
        equivalent_possible = False
        penalties.append("missing comparable size")
        score += 0.05

    attrs_match, has_missing_attr, attr_reasons, attr_penalties = _critical_attribute_result(reference, candidate)
    reasons.extend(attr_reasons)
    penalties.extend(attr_penalties)
    if not attrs_match:
        return MatchResult(
            decision="different",
            score=min(score, 0.45),
            fingerprint=candidate,
            product=product,
            reasons=reasons,
            penalties=penalties,
        )

    if has_missing_attr:
        equivalent_possible = False
        score += 0.12
    else:
        score += 0.25
        reasons.append("no critical attribute conflicts")

    brand_allowed, brand_reason = brand_allows_equivalence(reference, candidate)
    if brand_allowed:
        score += 0.15
        reasons.append(brand_reason)
    else:
        equivalent_possible = False
        penalties.append(brand_reason)
        score += 0.04

    token_similarity = _token_similarity(reference, candidate)
    score += token_similarity * 0.15
    reasons.append(f"token similarity: {token_similarity:.2f}")

    score = min(round(score, 4), 1.0)
    if equivalent_possible and score >= equivalence_threshold:
        decision = "equivalent"
    elif score >= 0.62:
        decision = "substitute"
    else:
        decision = "different"

    return MatchResult(
        decision=decision,
        score=score,
        fingerprint=candidate,
        product=product,
        reasons=reasons,
        penalties=penalties,
    )
