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
    def remove_duplicate_sku_ids(cls, sku_ids: list[UUID]) -> list[UUID]:
        return list(set(sku_ids))


class CreateDiscountOutputDTO(BaseModel):
    id: UUID = Field(
        description="Id of the discount",
    )
