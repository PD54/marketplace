from uuid import UUID

from pydantic import BaseModel, Field


class CancelDiscountInputDTO(BaseModel):
    id: UUID = Field(
        description="Id of the discount",
    )
