from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class NormalizedBaseModel(BaseModel):
    model_config = ConfigDict(
        str_strip_whitespace=True,
        validate_assignment=True,
        extra='forbid',
    )


class NormalizedLocation(NormalizedBaseModel):
    retailer: str
    location_id: str
    name: str
    address: str | None = None
    city: str | None = None
    state: str | None = None
    postal_code: str | None = None
    phone: str | None = None
    latitude: float | None = None
    longitude: float | None = None
    distance: str | None = None
    is_open: bool | None = None
    open_text: str | None = None
    service_type: str | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)


class NormalizedProduct(NormalizedBaseModel):
    retailer: str
    product_id: str | None = Field(
        default=None,
        description="Retailer-specific product identifier; optional when source data omits a stable ID.",
    )
    location_id: str | None = None
    name: str
    brand: str | None = None
    size: str | None = None
    price: float | None = None
    price_display: str | None = None
    unit_price: str | None = None
    promo_price: str | None = None
    was_price: str | None = None
    rating: float | None = None
    reviews: int | None = None
    image_url: str | None = None
    in_stock: bool | None = None
    availability: str | None = None
    stock_level: str | None = None
    url: str | None = None
    description: str | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)


def normalize_location(data: dict[str, Any]) -> dict[str, Any]:
    return NormalizedLocation.model_validate(data).model_dump()


def normalize_product(data: dict[str, Any]) -> dict[str, Any]:
    return NormalizedProduct.model_validate(data).model_dump()
