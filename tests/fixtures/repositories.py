import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.repositories.acceptance import AcceptanceRepository
from app.database.repositories.discount import DiscountRepository
from app.database.repositories.good import GoodRepository
from app.database.repositories.posting import PostingRepository
from app.database.repositories.posting_good import PostingGoodRepository
from app.database.repositories.sku import SkuRepository
from app.database.repositories.sku_and_discount import SkuAndDiscountRepository
from app.database.repositories.task import TaskRepository


@pytest.fixture
def good_repository(db_session: AsyncSession) -> GoodRepository:
    return GoodRepository(db_session)


@pytest.fixture
def sku_repository(db_session: AsyncSession) -> SkuRepository:
    return SkuRepository(db_session)


@pytest.fixture
def task_repository(db_session: AsyncSession) -> TaskRepository:
    return TaskRepository(db_session)


@pytest.fixture
def acceptance_repository(db_session: AsyncSession) -> AcceptanceRepository:
    return AcceptanceRepository(db_session)


@pytest.fixture
def posting_good_repository(db_session: AsyncSession) -> PostingGoodRepository:
    return PostingGoodRepository(db_session)


@pytest.fixture
def posting_repository(db_session: AsyncSession) -> PostingRepository:
    return PostingRepository(db_session)


@pytest.fixture
def discount_repository(db_session: AsyncSession) -> DiscountRepository:
    return DiscountRepository(db_session)


@pytest.fixture
def sku_and_discount_repository(
    db_session: AsyncSession,
) -> SkuAndDiscountRepository:
    return SkuAndDiscountRepository(db_session)
