from rapidfuzz import fuzz

from app.matching.models import ProductFingerprint
from app.matching.normalizer import normalize_text


def _jaccard_score(reference: ProductFingerprint, candidate: ProductFingerprint) -> float:
    left = set(reference.tokens)
    right = set(candidate.tokens)
    if not left or not right:
        return 0.0
    return len(left & right) / len(left | right)


def _ratio(value: float) -> float:
    return round(value / 100, 4)


def similarity_score(reference: ProductFingerprint, candidate: ProductFingerprint) -> tuple[float, list[str]]:
    reference_text = normalize_text(reference.source_name)
    candidate_text = normalize_text(candidate.source_name)

    token_set = _ratio(fuzz.token_set_ratio(reference_text, candidate_text))
    wratio = _ratio(fuzz.WRatio(reference_text, candidate_text))
    token_sort = _ratio(fuzz.token_sort_ratio(reference_text, candidate_text))
    jaccard = round(_jaccard_score(reference, candidate), 4)

    score = round(
        0.45 * token_set
        + 0.25 * wratio
        + 0.20 * token_sort
        + 0.10 * jaccard,
        4,
    )
    reasons = [
        f"token_set similarity: {token_set:.2f}",
        f"weighted ratio similarity: {wratio:.2f}",
        f"token_sort similarity: {token_sort:.2f}",
        f"token jaccard similarity: {jaccard:.2f}",
    ]
    return score, reasons


def rank_score(rule_score: float, similarity: float) -> float:
    return round((0.70 * rule_score) + (0.30 * similarity), 4)
