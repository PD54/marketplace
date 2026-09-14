import pytest

from app.database.dto.acceptance import AcceptanceDTO
from app.database.dto.good import GoodDTO
from app.database.dto.posting import PostingDTO
from app.database.dto.posting_good import PostingGoodDTO
from app.database.dto.sku import SkuDTO
from app.database.dto.task import TaskDTO
from app.database.repositories.acceptance import AcceptanceRepository
from app.database.repositories.good import GoodRepository
from app.database.repositories.posting import PostingRepository
from app.database.repositories.posting_good import PostingGoodRepository
from app.database.repositories.sku import SkuRepository
from app.database.repositories.task import TaskRepository


@pytest.fixture
async def sku_in_db(
    sku_repository: SkuRepository,
    sku: SkuDTO,
) -> SkuDTO:
    return await sku_repository.create(sku)


@pytest.fixture
async def good_in_db(
    good_repository: GoodRepository,
    good: GoodDTO,
    sku_in_db: SkuDTO,
) -> GoodDTO:
    return await good_repository.create(good)


@pytest.fixture
async def reserved_good_in_db(
    good_repository: GoodRepository,
    reserved_good: GoodDTO,
    sku_in_db: SkuDTO,
) -> GoodDTO:
    return await good_repository.create(reserved_good)


@pytest.fixture
async def posting_in_db(
    posting_repository: PostingRepository,
    posting: PostingDTO,
) -> PostingDTO:
    return await posting_repository.create(posting)


@pytest.fixture
async def posting_good_in_db(
    posting_good_repository: PostingGoodRepository,
    posting_good: PostingGoodDTO,
    posting_in_db: PostingDTO,
    reserved_good_in_db: GoodDTO,
) -> PostingGoodDTO:
    return await posting_good_repository.create(posting_good)


@pytest.fixture
async def tasks_from_posting_in_db(
    task_repository: TaskRepository,
    tasks_from_posting_list: list[TaskDTO],
    posting_in_db: PostingDTO,
    reserved_good_in_db: GoodDTO,
) -> list[TaskDTO]:
    return await task_repository.bulk_create(tasks_from_posting_list)


@pytest.fixture
async def acceptance_in_db(
    acceptance_repository: AcceptanceRepository,
    acceptance: AcceptanceDTO,
) -> AcceptanceDTO:
    return await acceptance_repository.create(acceptance)


@pytest.fixture
async def tasks_from_acceptance_in_db(
    task_repository: TaskRepository,
    tasks_from_acceptance_list: list[TaskDTO],
    acceptance_in_db: AcceptanceDTO,
    sku_in_db: SkuDTO,
) -> list[TaskDTO]:
    return await task_repository.bulk_create(tasks_from_acceptance_list)
