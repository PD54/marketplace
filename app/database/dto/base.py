from datetime import UTC, datetime
from uuid import UUID, uuid7

from pydantic import BaseModel, ConfigDict, Field


class BaseDTO(BaseModel):
    id: UUID = Field(
        default_factory=uuid7,
        description="Id of the entity",
    )
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC),
        description="Timestamp of entity creation",
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC),
        description="Timestamp of last entity update",
    )

    model_config = ConfigDict(from_attributes=True)
