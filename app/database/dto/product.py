from uuid import UUID
from enum import StrEnum

from pydantic import Field

from app.database.dto.base import BaseDTO


class ProductStock(StrEnum):
    valid = "valid"
    defect = "defect"
    not_found = "not_found"


class ProductDTO(BaseDTO):
    sku_id: UUID = Field(
        ...,
        description=(
            "UUIDv7 of the SKU that the product belongs to "
            "(foreign key)"
        )
    )
    stock: ProductStock = Field(
        default=ProductStock.valid,
        description="Stock status of the product."
    )
    reserved_state: bool = Field(
        default=False,
        description="Flag that tells if the product is reserved"
    )
