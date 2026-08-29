from uuid import UUID

from pydantic import BaseModel, Field


class ToggleIsHiddenInputDTO(BaseModel):
    sku_id: UUID = Field(
        description="Id of the sku to toggle is_hidden",
    )
    is_hidden: bool = Field(
        description="New value for the 'is_hidden' field",
    )
