from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from app.database.dto.good import GoodStockWithoutNotFound
from app.database.dto.task import TaskStatus


class GetAcceptanceInfoAcceptedItemOutputDTO(BaseModel):
    sku_id: UUID = Field(
        description="SKU id of the accepted goods",
    )
    stock: GoodStockWithoutNotFound = Field(
        description="Stock type of the accepted goods",
    )
    count: int = Field(
        description="Number of the accepted goods",
    )

    model_config = ConfigDict(from_attributes=True)


class GetAcceptanceInfoTaskOutputDTO(BaseModel):
    id: UUID = Field(
        description="Id of the task",
    )
    status: TaskStatus = Field(
        description="Task status of the task",
    )

    model_config = ConfigDict(from_attributes=True)


class GetAcceptanceInfoOutputDTO(BaseModel):
    id: UUID = Field(
        description="Id of the acceptance",
    )
    created_at: datetime = Field(
        description="Timestamp of the acceptance creation",
    )
    accepted: list[GetAcceptanceInfoAcceptedItemOutputDTO] = Field(
        description="List of accepted items",
    )
    task_ids: list[GetAcceptanceInfoTaskOutputDTO] = Field(
        description="List of tasks belonging to the acceptance",
    )

    model_config = ConfigDict(from_attributes=True)
