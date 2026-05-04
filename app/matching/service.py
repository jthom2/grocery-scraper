from typing import Any

from app.matching.models import MatchSearchResponse
from app.matching.normalizer import fingerprint_product, fingerprint_query
from app.matching.scorer import score_fingerprints


SUPPORTED_RETAILERS = ("aldi", "kroger", "publix", "walmart")


def match_products(
    query: str,
    products: list[dict[str, Any]],
    equivalence_threshold: float = 0.82,
    errors: dict[str, str] | None = None,
) -> MatchSearchResponse:
    canonical = fingerprint_query(query)
    equivalent = []
    substitutes = []
    rejected = []

    for product in products:
        fingerprint = fingerprint_product(product)
        result = score_fingerprints(
            canonical,
            fingerprint,
            product=product,
            equivalence_threshold=equivalence_threshold,
        )

        if result.decision == "equivalent":
            equivalent.append(result)
        elif result.decision == "substitute":
            substitutes.append(result)
        else:
            rejected.append(result)

    equivalent.sort(key=lambda item: item.score, reverse=True)
    substitutes.sort(key=lambda item: item.score, reverse=True)
    rejected.sort(key=lambda item: item.score, reverse=True)

    return MatchSearchResponse(
        query=query,
        canonical_fingerprint=canonical,
        equivalent=equivalent,
        substitutes=substitutes,
        rejected=rejected,
        errors=errors or {},
    )
