from datetime import datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, Field

from app.database.dto.discount import DiscountStatus


class GetDiscountOutputDTO(BaseModel):
    id: UUID = Field(
        description="Id of the discount",
    )
    status: DiscountStatus = Field(
        description="Status of the discount",
    )
    created_at: datetime = Field(
        description="Timestamp of the discount creation",
    )
    percentage: Decimal = Field(
        description="The percentage of the discount",
    )
    sku_ids: list[UUID] = Field(
        description="A list of SKU ids associated with this discount",
    )
