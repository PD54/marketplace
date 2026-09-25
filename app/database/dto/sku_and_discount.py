from uuid import UUID

from pydantic import Field

from app.database.dto.base import BaseDTO, UpdateBaseDTO


class SkuAndDiscountDTO(BaseDTO):
    sku_id: UUID = Field(
        description="Id of the SKU",
    )
    discount_id: UUID = Field(
        description="Id of the discount",
    )


class UpdateSkuAndDiscountDTO(UpdateBaseDTO):
    sku_id: UUID | None = Field(
        None,
        description="Id of the SKU",
    )
    discount_id: UUID | None = Field(
        None,
        description="Id of the discount",
    )
