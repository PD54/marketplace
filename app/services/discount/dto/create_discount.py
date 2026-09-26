from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, Field, field_validator


class CreateDiscountInputDTO(BaseModel):
    sku_ids: list[UUID] = Field(
        min_length=1,
        description="A list of SKU ids associated with this discount",
    )
    percentage: Decimal = Field(
        description="The percentage of the discount",
    )

    @field_validator("sku_ids")
    @classmethod
    def validate_unique_sku_ids(cls, sku_ids: list[UUID]) -> list[UUID]:
        if len(sku_ids) != len(set(sku_ids)):
            raise ValueError("SKU ids must be unique")
        return sku_ids


class CreateDiscountOutputDTO(BaseModel):
    id: UUID = Field(
        description="Id of the discount",
    )
