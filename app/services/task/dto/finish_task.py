from uuid import UUID

from pydantic import BaseModel, Field

from app.database.dto.task import TaskStatusWithoutInWork


class FinishTaskInputDTO(BaseModel):
    id: UUID = Field(
        description="Id of the task",
    )
    status: TaskStatusWithoutInWork = Field(
        description="Task finishing status",
    )
