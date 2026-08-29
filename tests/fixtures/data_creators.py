import pytest

from app.database.dto.acceptance import AcceptanceDTO
from app.database.dto.good import GoodDTO
from app.database.dto.sku import SkuDTO
from app.database.dto.task import TaskDTO
from app.database.repositories.acceptance import AcceptanceRepository
from app.database.repositories.good import GoodRepository
from app.database.repositories.sku import SkuRepository
from app.database.repositories.task import TaskRepository


@pytest.fixture
async def sku_in_db(
    sku_repository: SkuRepository,
    sku_dto: SkuDTO,
) -> SkuDTO:
    return await sku_repository.create(sku_dto)


@pytest.fixture
async def good_in_db(
    good_repository: GoodRepository,
    good_dto: GoodDTO,
    sku_in_db: SkuDTO,
) -> GoodDTO:
    return await good_repository.create(good_dto)


@pytest.fixture
async def acceptance_in_db(
    acceptance_repository: AcceptanceRepository,
    acceptance_dto: AcceptanceDTO,
) -> AcceptanceDTO:
    return await acceptance_repository.create(acceptance_dto)


@pytest.fixture
async def tasks_from_acceptance_in_db(
    task_repository: TaskRepository,
    tasks_from_acceptance_list: list[TaskDTO],
    acceptance_in_db: AcceptanceDTO,
    sku_in_db: SkuDTO,
) -> list[TaskDTO]:
    return await task_repository.bulk_create(tasks_from_acceptance_list)
