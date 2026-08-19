from uuid import UUID

from pydantic import BaseModel, Field, ConfigDict

from app.database.dto.good import GoodStockWithoutNotFound


class CreateAcceptanceItemInputDTO(BaseModel):
    sku_id: UUID = Field(
        description="Id of the sku of goods which must be placed"
    )
    stock: GoodStockWithoutNotFound = Field(
        description="Stock type in which goods must be placed"
    )
    count: int = Field(
        gt=0,
        lt=1000,
        description="The count of goods to place"
    )


class CreateAcceptanceInputDTO(BaseModel):
    items_to_accept: list[CreateAcceptanceItemInputDTO] = Field(
        min_length=1,
        description="List of items to accept"
    )

    model_config = ConfigDict(from_attributes=True)


class CreateAcceptanceOutputDTO(BaseModel):
    id: UUID = Field(description="Id of the acceptance")

    model_config = ConfigDict(from_attributes=True)
