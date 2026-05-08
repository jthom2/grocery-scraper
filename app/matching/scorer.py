from typing import Any

from app.matching.brands import brand_allows_equivalence
from app.matching.models import MatchResult, ProductFingerprint
from app.matching.rules import (
    CRITICAL_ATTRIBUTES,
    GENERAL_EQUIVALENCE_TOKEN_THRESHOLD,
    REJECT_SCORES,
    SCORE_WEIGHTS,
    STRICT_CATEGORIES,
    SUBSTITUTE_THRESHOLD,
)
from app.matching.units import sizes_compatible


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

    for attr in CRITICAL_ATTRIBUTES.get(reference.category or "", ()):
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


def _is_strict_category(category: str | None) -> bool:
    return bool(category and category in STRICT_CATEGORIES)


def _category_result(reference: ProductFingerprint, candidate: ProductFingerprint) -> tuple[bool, bool, str]:
    ref_category = reference.category
    candidate_category = candidate.category

    if ref_category and candidate_category and ref_category == candidate_category:
        return True, _is_strict_category(ref_category), f"same category: {ref_category}"

    if _is_strict_category(ref_category) or _is_strict_category(candidate_category):
        return False, False, f"category mismatch: {ref_category or 'unknown'} vs {candidate_category or 'unknown'}"

    return True, False, (
        f"general category fallback: {ref_category or 'unknown'} vs "
        f"{candidate_category or 'unknown'}"
    )


def _has_national_brand_conflict(reference: ProductFingerprint, candidate: ProductFingerprint) -> bool:
    same_brand = bool(reference.normalized_brand and reference.normalized_brand == candidate.normalized_brand)
    return not same_brand and (
        reference.brand_class == "national_brand" or candidate.brand_class == "national_brand"
    )


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

    categories_compatible, strict_category_match, category_reason = _category_result(reference, candidate)
    if not categories_compatible:
        penalties.append(category_reason)
        return MatchResult(
            decision="different",
            score=0.0,
            fingerprint=candidate,
            product=product,
            reasons=reasons,
            penalties=penalties,
        )

    if strict_category_match:
        score += SCORE_WEIGHTS["category"]
    else:
        score += SCORE_WEIGHTS["general_category"]
    reasons.append(category_reason)

    if reference.size and candidate.size:
        if not sizes_compatible(reference.size, candidate.size):
            penalties.append(
                f"size conflict: {reference.size.value:g} {reference.size.unit} vs "
                f"{candidate.size.value:g} {candidate.size.unit}"
            )
            return MatchResult(
                decision="different",
                score=REJECT_SCORES["size_conflict"],
                fingerprint=candidate,
                product=product,
                reasons=reasons,
                penalties=penalties,
            )
        score += SCORE_WEIGHTS["size_match"]
        reasons.append(f"same normalized size: {reference.size.value:g} {reference.size.unit}")
    else:
        equivalent_possible = False
        penalties.append("missing comparable size")
        score += SCORE_WEIGHTS["missing_size"]

    attrs_match, has_missing_attr, attr_reasons, attr_penalties = _critical_attribute_result(reference, candidate)
    reasons.extend(attr_reasons)
    penalties.extend(attr_penalties)
    if not attrs_match:
        return MatchResult(
            decision="different",
            score=min(score, REJECT_SCORES["attribute_conflict_cap"]),
            fingerprint=candidate,
            product=product,
            reasons=reasons,
            penalties=penalties,
        )

    if has_missing_attr:
        equivalent_possible = False
        score += SCORE_WEIGHTS["attribute_missing"]
    else:
        score += SCORE_WEIGHTS["attribute_match"]
        reasons.append("no critical attribute conflicts")

    brand_allowed, brand_reason = brand_allows_equivalence(reference, candidate)
    if brand_allowed:
        score += SCORE_WEIGHTS["brand_match"]
        reasons.append(brand_reason)
    else:
        if _has_national_brand_conflict(reference, candidate):
            penalties.append(brand_reason)
            return MatchResult(
                decision="different",
                score=min(score, REJECT_SCORES["brand_conflict_cap"]),
                fingerprint=candidate,
                product=product,
                reasons=reasons,
                penalties=penalties,
            )
        equivalent_possible = False
        penalties.append(brand_reason)
        score += SCORE_WEIGHTS["brand_mismatch"]

    token_similarity = _token_similarity(reference, candidate)
    score += token_similarity * SCORE_WEIGHTS["token_similarity"]
    reasons.append(f"token similarity: {token_similarity:.2f}")

    if not strict_category_match and token_similarity < GENERAL_EQUIVALENCE_TOKEN_THRESHOLD:
        equivalent_possible = False
        penalties.append(
            f"general category token similarity below {GENERAL_EQUIVALENCE_TOKEN_THRESHOLD:.2f}"
        )

    score = min(round(score, 4), 1.0)
    if equivalent_possible and score >= equivalence_threshold:
        decision = "equivalent"
    elif score >= SUBSTITUTE_THRESHOLD:
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
