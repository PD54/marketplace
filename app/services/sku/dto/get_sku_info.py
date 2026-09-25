from datetime import datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, Field


class GetSkuInfoOutputDTO(BaseModel):
    id: UUID = Field(
        description="Id of the SKU",
    )
    created_at: datetime = Field(
        description="Timestamp of the SKU creation",
    )
    actual_price: Decimal = Field(
        description="Actual price of the SKU with max discount applied",
    )
    base_price: Decimal = Field(
        description="Base price of the SKU",
    )
    count: int = Field(
        description="Count of the goods belonging to the SKU",
    )
    is_hidden: bool = Field(
        description="Flag that tells if this SKU is hidden",
    )
