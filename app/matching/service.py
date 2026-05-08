from typing import Any

from app.matching.models import MatchResult, MatchSearchResponse, RetailerMatchGroup
from app.matching.normalizer import fingerprint_product, fingerprint_query, normalize_text
from app.matching.scorer import score_fingerprints
from app.matching.similarity import rank_score, similarity_score


SUPPORTED_RETAILERS = ("aldi", "kroger", "publix", "walmart")


def _result_sort_key(result):
    fingerprint = result.fingerprint
    return (
        -result.rank_score,
        -result.similarity_score,
        -result.score,
        fingerprint.retailer or "",
        fingerprint.product_id or "",
        fingerprint.source_name,
    )


def _product_retailer(product: dict[str, Any]) -> str:
    return str(product.get("retailer") or "unknown").lower()


def _dedupe_key(product: dict[str, Any]) -> tuple[str, str]:
    retailer = _product_retailer(product)
    product_id = product.get("product_id")
    if product_id:
        return retailer, f"id:{product_id}"

    name = normalize_text(str(product.get("name") or ""))
    location_id = str(product.get("location_id") or "")
    return retailer, f"name:{name}:{location_id}"


def _group_status(candidates: list[MatchResult], error: str | None = None) -> tuple[str, MatchResult | None]:
    if error:
        return "error", None

    for result in candidates:
        if result.decision in {"equivalent", "substitute"}:
            return result.decision, result

    return "no_match", None


def match_products(
    query: str,
    products: list[dict[str, Any]],
    retailers: list[str] | None = None,
    max_candidates_per_retailer: int = 24,
    equivalence_threshold: float = 0.82,
    errors: dict[str, str] | None = None,
) -> MatchSearchResponse:
    canonical = fingerprint_query(query)
    deduped: dict[tuple[str, str], dict[str, Any]] = {}

    for product in products:
        fingerprint = fingerprint_product(product)
        similarity, similarity_reasons = similarity_score(canonical, fingerprint)
        entry = {
            "product": product,
            "fingerprint": fingerprint,
            "similarity_score": similarity,
            "similarity_reasons": similarity_reasons,
        }
        key = _dedupe_key(product)
        existing = deduped.get(key)
        if existing is None or similarity > existing["similarity_score"]:
            deduped[key] = entry

    entries_by_retailer: dict[str, list[dict[str, Any]]] = {}
    for entry in deduped.values():
        retailer = entry["fingerprint"].retailer or _product_retailer(entry["product"])
        entries_by_retailer.setdefault(retailer, []).append(entry)

    errors = errors or {}
    retailer_order = list(dict.fromkeys([
        *(retailer.lower() for retailer in (retailers or [])),
        *entries_by_retailer.keys(),
        *errors.keys(),
    ]))

    matches_by_retailer = {}
    for retailer in retailer_order:
        ranked_entries = sorted(
            entries_by_retailer.get(retailer, []),
            key=lambda entry: (
                -entry["similarity_score"],
                entry["fingerprint"].product_id or "",
                entry["fingerprint"].source_name,
            ),
        )[:max_candidates_per_retailer]

        candidates = []
        for entry in ranked_entries:
            fingerprint = entry["fingerprint"]
            similarity = entry["similarity_score"]
            result = score_fingerprints(
                canonical,
                fingerprint,
                product=entry["product"],
                equivalence_threshold=equivalence_threshold,
            )
            result = result.model_copy(update={
                "similarity_score": similarity,
                "rank_score": rank_score(result.score, similarity),
                "similarity_reasons": entry["similarity_reasons"],
            })
            candidates.append(result)

        candidates.sort(key=_result_sort_key)
        error = errors.get(retailer)
        status, best = _group_status(candidates, error=error)
        matches_by_retailer[retailer] = RetailerMatchGroup(
            retailer=retailer,
            status=status,
            best=best,
            candidates=candidates,
            error=error,
        )

    return MatchSearchResponse(
        query=query,
        canonical_fingerprint=canonical,
        matches_by_retailer=matches_by_retailer,
        errors=errors,
    )
