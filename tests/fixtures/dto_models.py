from decimal import Decimal
from uuid import uuid7

import pytest

from app.database.dto.acceptance import AcceptanceDTO
from app.database.dto.good import GoodDTO, GoodStock
from app.database.dto.posting import PostingDTO
from app.database.dto.posting_good import PostingGoodDTO
from app.database.dto.sku import SkuDTO
from app.database.dto.task import TaskDTO, TaskStatus, TaskType


@pytest.fixture
def good(sku: SkuDTO) -> GoodDTO:
    return GoodDTO(sku_id=sku.id)


@pytest.fixture
def reserved_good(sku: SkuDTO) -> GoodDTO:
    return GoodDTO(
        sku_id=sku.id,
        reserved_state=True,
    )


@pytest.fixture
def sku() -> SkuDTO:
    return SkuDTO(base_price=Decimal("5000.00"))


@pytest.fixture
def acceptance() -> AcceptanceDTO:
    return AcceptanceDTO()


@pytest.fixture
def posting() -> PostingDTO:
    return PostingDTO()


@pytest.fixture
def posting_good(
    posting: PostingGoodDTO,
    reserved_good: GoodDTO,
    sku: SkuDTO,
) -> PostingGoodDTO:
    return PostingGoodDTO(
        posting_id=posting.id,
        good_id=reserved_good.id,
        good_sku_id=sku.id,
        good_cost=Decimal("4000.00"),
        good_stock=reserved_good.stock,
    )


@pytest.fixture
def task_from_acceptance(
    acceptance: AcceptanceDTO,
    sku: SkuDTO,
) -> TaskDTO:
    return TaskDTO(
        status=TaskStatus.completed,
        task_type=TaskType.placing,
        acceptance_id=acceptance.id,
        sku_id=sku.id,
        stock=GoodStock.valid,
        count=25,
    )


@pytest.fixture
def task_from_posting(
    posting: PostingDTO,
    reserved_good: GoodDTO,
) -> TaskDTO:
    return TaskDTO(
        status=TaskStatus.completed,
        task_type=TaskType.picking,
        posting_id=posting.id,
        sku_id=reserved_good.sku_id,
        good_id=reserved_good.id,
        stock=reserved_good.stock,
        count=1,
    )


@pytest.fixture
def tasks_from_acceptance_list(
    task_from_acceptance: TaskDTO,
) -> list[TaskDTO]:
    completed_task = task_from_acceptance
    in_work_task = task_from_acceptance.model_copy(
        update={
            "id": uuid7(),
            "status": TaskStatus.in_work,
        }
    )
    cancelled_task = task_from_acceptance.model_copy(
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


@pytest.fixture
def tasks_from_posting_list(
    task_from_posting: TaskDTO,
) -> list[TaskDTO]:
    completed_task = task_from_posting
    in_work_task = task_from_posting.model_copy(
        update={
            "id": uuid7(),
            "status": TaskStatus.in_work,
        }
    )
    cancelled_task = task_from_posting.model_copy(
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
