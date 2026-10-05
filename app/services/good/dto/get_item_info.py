from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.database.dto.good import GoodReservedState, GoodStock


class GetItemInfoOutputDTO(BaseModel):
    id: UUID = Field(
        description="Id of the good",
    )
    sku_id: UUID = Field(
        description="Id of the SKU that the good belongs to (foreign key)",
    )
    stock: GoodStock = Field(
        description="Stock status of the good.",
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

    model_config = ConfigDict(from_attributes=True)
