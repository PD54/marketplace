from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, Field


class MarkdownItemInputDTO(BaseModel):
    id: UUID = Field(
        description="Id of the good",
    )
    percentage: Decimal = Field(
        description="Discount percentage of the good",
        ge=Decimal("0.00"),
        le=Decimal("100.00"),
    )
