from uuid import UUID
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class CreateSkuInputDTO(BaseModel):
    id: UUID = Field(
        description="Id of the sku"
    )
    base_price: Decimal = Field(
        ge=Decimal("0.00"),
        description="Base price of the SKU"
    )
    is_hidden: bool = Field(
        description="Flag that tells if this SKU is hidden"
    )

    model_config = ConfigDict(from_attributes=True)


class CreateSkuOutputDTO(BaseModel):
    id: UUID = Field(
        description="Id of the sku"
    )
    base_price: Decimal = Field(
        description="Base price of the SKU"
    )
    is_hidden: bool = Field(
        description="Flag that tells if this SKU is hidden"
    )

    model_config = ConfigDict(from_attributes=True)
