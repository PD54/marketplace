from uuid import UUID

from pydantic import BaseModel, Field

from app.database.dto.good import GoodStock


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


class GetItemInfoBySkuIdOutputDTO(BaseModel):
    items: list[GetItemInfoBySkuIdItemOutputDTO] = Field(
        description="List of goods that belong to the SKU",
    )
