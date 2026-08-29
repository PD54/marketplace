from uuid import UUID

from pydantic import BaseModel, Field


class MoveToNotFoundInputDTO(BaseModel):
    id: UUID = Field(
        description="Id of the good that must be moved to not_found stock",
    )
