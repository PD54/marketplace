from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, Field


class SetSkuPriceInputDTO(BaseModel):
    sku_id: UUID = Field(
        description="Id of the SKU",
    )
    base_price: Decimal = Field(
        description="Base price of the SKU",
        ge=Decimal("0.00"),
    )
