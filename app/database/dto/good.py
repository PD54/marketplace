from decimal import Decimal
from enum import StrEnum
from typing import Literal
from uuid import UUID

from pydantic import Field

from app.database.dto.base import BaseDTO, UpdateBaseDTO


class GoodReservedState(StrEnum):
    unreserved = "unreserved"
    reserved = "reserved"
    sold = "sold"


class GoodStock(StrEnum):
    valid = "valid"
    defect = "defect"
    not_found = "not_found"


GoodStockWithoutNotFound = Literal[GoodStock.valid, GoodStock.defect]


class GoodDTO(BaseDTO):
    sku_id: UUID = Field(
        description="Id of the SKU that the good belongs to (foreign key)",
    )
    stock: GoodStock = Field(
        GoodStock.valid,
        description="Stock status of the good.",
    )
    reserved_state: GoodReservedState = Field(
        GoodReservedState.unreserved,
        description="Reservation status of the good",
    )
    discount_percentage: Decimal = Field(
        Decimal("0.00"),
        description="Discount percentage of the good",
    )


class UpdateGoodDTO(UpdateBaseDTO):
    sku_id: UUID | None = Field(
        None,
        description="Id of the SKU that the good belongs to (foreign key)",
    )
    stock: GoodStock | None = Field(
        None,
        description="Stock status of the good.",
    )
    reserved_state: GoodReservedState | None = Field(
        None,
        description="Reservation status of the good",
    )
    discount_percentage: Decimal | None = Field(
        None,
        description="Discount percentage of the good",
    )
