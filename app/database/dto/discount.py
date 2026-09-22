from decimal import Decimal
from enum import StrEnum

from pydantic import Field

from app.database.dto.base import BaseDTO, UpdateBaseDTO


class DiscountStatus(StrEnum):
    active = "active"
    finished = "finished"


class DiscountDTO(BaseDTO):
    status: DiscountStatus = Field(
        DiscountStatus.active,
        description="The status of the discount",
    )
    percentage: Decimal = Field(
        Decimal("0.00"),
        description="The percentage of the discount",
    )


class UpdateDiscountDTO(UpdateBaseDTO):
    status: DiscountStatus | None = Field(
        None,
        description="The status of the discount",
    )
    percentage: Decimal | None = Field(
        None,
        description="The percentage of the discount",
    )
