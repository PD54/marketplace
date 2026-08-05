from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from app.database.dto.good import GoodStock


class GetItemInfoOutputDTO(BaseModel):
    id: UUID = Field(
        description="Id of the good"
    )
    sku_id: UUID = Field(
        description=(
            "Id of the SKU that the good belongs to "
            "(foreign key)"
        )
    )
    stock: GoodStock = Field(
        description=(
            "Stock status of the good."
        )
    )
    reserved_state: bool = Field(
        description="Flag that tells if the good is reserved"
    )

    model_config = ConfigDict(from_attributes=True)
