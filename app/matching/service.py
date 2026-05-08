from typing import Any

from app.matching.models import MatchSearchResponse
from app.matching.normalizer import fingerprint_product, fingerprint_query
from app.matching.scorer import score_fingerprints


SUPPORTED_RETAILERS = ("aldi", "kroger", "publix", "walmart")


def _result_sort_key(result):
    fingerprint = result.fingerprint
    return (
        -result.score,
        fingerprint.retailer or "",
        fingerprint.product_id or "",
        fingerprint.source_name,
    )


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

    equivalent.sort(key=_result_sort_key)
    substitutes.sort(key=_result_sort_key)
    rejected.sort(key=_result_sort_key)

    return MatchSearchResponse(
        query=query,
        canonical_fingerprint=canonical,
        equivalent=equivalent,
        substitutes=substitutes,
        rejected=rejected,
        errors=errors or {},
    )
