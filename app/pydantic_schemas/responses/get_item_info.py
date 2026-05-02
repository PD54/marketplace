from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from app.models.stock_enum import ProductStock


class GetItemInfoResponse(BaseModel):
    id: UUID = Field(
        description="UUIDv7 of the product"
    )
    sku_id: UUID = Field(
        description=(
            "UUIDv7 of the SKU that the product belongs to "
            "(foreign key)"
        )
    )
    stock: ProductStock = Field(
        description=(
            "Stock status of the product."
        )
    )
    reserved_state: bool = Field(
        description="Flag that tells if the product is reserved"
    )

    model_config = ConfigDict(from_attributes=True)
