import pytest

from app.database.dto.acceptance import AcceptanceDTO
from app.database.dto.good import GoodDTO
from app.database.dto.posting import PostingDTO
from app.database.dto.sku import SkuDTO
from app.database.dto.task import TaskDTO
from app.database.repositories.task import TaskRepository


@pytest.fixture
async def task_picking_in_work_in_db(
    sku_in_db: SkuDTO,
    posting_in_db: PostingDTO,
    good_reserved_in_db: GoodDTO,
    task_picking_in_work: TaskDTO,
    task_repository: TaskRepository,
) -> TaskDTO:
    return await task_repository.create(task_picking_in_work)


@pytest.fixture
async def tasks_from_acceptance_in_db(
    task_repository: TaskRepository,
    tasks_from_acceptance_list: list[TaskDTO],
    acceptance_in_db: AcceptanceDTO,
    sku_in_db: SkuDTO,
) -> list[TaskDTO]:
    return await task_repository.bulk_create(tasks_from_acceptance_list)
