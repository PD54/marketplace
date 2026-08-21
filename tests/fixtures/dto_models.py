from decimal import Decimal
from uuid import uuid7

import pytest

from app.database.dto.acceptance import AcceptanceDTO
from app.database.dto.good import GoodDTO, GoodStock
from app.database.dto.sku import SkuDTO
from app.database.dto.task import TaskDTO, TaskStatus, TaskType


@pytest.fixture
def good_dto(sku_dto: SkuDTO) -> GoodDTO:
    return GoodDTO(sku_id=sku_dto.id)


@pytest.fixture
def sku_dto() -> SkuDTO:
    return SkuDTO(base_price=Decimal("5000.00"))


@pytest.fixture
def acceptance_dto() -> AcceptanceDTO:
    return AcceptanceDTO()


@pytest.fixture
def task_dto(
    acceptance_dto: AcceptanceDTO,
    sku_dto: SkuDTO,
) -> TaskDTO:
    return TaskDTO(
        status=TaskStatus.completed,
        task_type=TaskType.placing,
        acceptance_id=acceptance_dto.id,
        sku_id=sku_dto.id,
        stock=GoodStock.valid,
        count=25,
    )


@pytest.fixture
def tasks_list(
    task_dto: TaskDTO,
) -> list[TaskDTO]:
    completed_task = task_dto
    in_work_task = task_dto.model_copy(
        update={
            "id": uuid7(),
            "status": TaskStatus.in_work,
        }
    )
    cancelled_task = task_dto.model_copy(
        update={
            "id": uuid7(),
            "status": TaskStatus.cancelled,
        }
    )

    list_of_tasks = [
        completed_task,
        in_work_task,
        cancelled_task,
    ]
    return list_of_tasks
