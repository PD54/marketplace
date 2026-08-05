from uuid import UUID
from enum import StrEnum

from pydantic import Field

from app.database.dto.base import BaseDTO
from app.database.dto.good import GoodStockWithoutNotFound


class TaskStatus(StrEnum):
    completed = "completed"
    in_work = "in_work"
    cancelled = "cancelled"


class TaskType(StrEnum):
    picking = "picking"
    placing = "placing"


class TaskDTO(BaseDTO):
    status: TaskStatus = Field(
        TaskStatus.in_work,
        description="Status of the task"
    )
    task_type: TaskType = Field(description="Type of the task")
    posting_id: UUID | None = Field(
        None,
        description="Id of the posting that the task is assigned to"
    )
    acceptance_id: UUID | None = Field(
        None,
        description="Id of the acceptance that the task is assigned to"
    )
    good_id: UUID | None = Field(
        None,
        description="Id of the good which is the target of the task"
    )
    sku_id: UUID = Field(
        description="Id of the sku which is the target of the task"
    )
    stock: GoodStockWithoutNotFound = Field(
        description="Stock status of target entity(ies) of the task"
    )
    count: int = Field(
        description="Number of target entity(ies) of the task"
    )
