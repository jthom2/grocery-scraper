from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field


MatchDecision = Literal["equivalent", "substitute", "different"]
RetailerMatchStatus = Literal["equivalent", "substitute", "no_match", "error"]
BrandClass = Literal["store_brand", "national_brand", "unknown"]
SizeUnit = Literal["fl_oz", "oz", "ct", "ml", "l", "each", "sq_ft"]


class MatchingBaseModel(BaseModel):
    model_config = ConfigDict(
        str_strip_whitespace=True,
        validate_assignment=True,
        extra="forbid",
    )


class ParsedSize(MatchingBaseModel):
    value: float
    unit: SizeUnit
    source: str | None = None


class ProductFingerprint(MatchingBaseModel):
    source_name: str
    retailer: str | None = None
    product_id: str | None = None
    brand: str | None = None
    normalized_brand: str | None = None
    brand_class: BrandClass = "unknown"
    category: str | None = None
    tokens: list[str] = Field(default_factory=list)
    size: ParsedSize | None = None
    attributes: dict[str, Any] = Field(default_factory=dict)
    is_query: bool = False


class MatchResult(MatchingBaseModel):
    decision: MatchDecision
    score: float
    similarity_score: float = 0.0
    rank_score: float = 0.0
    fingerprint: ProductFingerprint
    product: dict[str, Any] | None = None
    similarity_reasons: list[str] = Field(default_factory=list)
    reasons: list[str] = Field(default_factory=list)
    penalties: list[str] = Field(default_factory=list)


class RetailerMatchGroup(MatchingBaseModel):
    retailer: str
    status: RetailerMatchStatus
    best: MatchResult | None = None
    candidates: list[MatchResult] = Field(default_factory=list)
    error: str | None = None


class MatchSearchRequest(MatchingBaseModel):
    query: str = Field(..., min_length=1)
    retailers: list[str] | None = None
    zip_code: str | None = None
    max_candidates_per_retailer: int = Field(default=24, ge=1, le=50)
    equivalence_threshold: float = Field(default=0.82, ge=0, le=1)


class MatchSearchResponse(MatchingBaseModel):
    query: str
    canonical_fingerprint: ProductFingerprint
    matches_by_retailer: dict[str, RetailerMatchGroup] = Field(default_factory=dict)
    errors: dict[str, str] = Field(default_factory=dict)
