from uuid import UUID

from pydantic import BaseModel, Field, field_validator

from app.database.dto.good import GoodReservedState, GoodStock


class GetItemInfoBySkuIdItemOutputDTO(BaseModel):
    item_id: UUID = Field(
        description="Id of the good",
    )
    stock: GoodStock = Field(
        description="Stock status of the good",
    )
    reserved_state: bool = Field(
        description="Flag that tells if the good is reserved",
    )

    @field_validator("reserved_state", mode="before")
    @classmethod
    def convert_reserved_state_to_bool(
        cls,
        value: GoodReservedState | bool,
    ) -> bool:
        if isinstance(value, GoodReservedState):
            return value != GoodReservedState.unreserved
        return value


class GetItemInfoBySkuIdOutputDTO(BaseModel):
    items: list[GetItemInfoBySkuIdItemOutputDTO] = Field(
        description="List of goods that belong to the SKU",
    )
