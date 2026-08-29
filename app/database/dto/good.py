from enum import StrEnum
from typing import Literal
from uuid import UUID

from pydantic import Field

from app.database.dto.base import BaseDTO, UpdateBaseDTO


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
    reserved_state: bool = Field(
        False,
        description="Flag that tells if the good is reserved",
    )


class UpdateGoodDTO(UpdateBaseDTO):
    stock: GoodStock | None = Field(
        None,
        description="Stock status of the good.",
    )
    reserved_state: bool | None = Field(
        None,
        description="Flag that tells if the good is reserved",
    )
