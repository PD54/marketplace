import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.repositories.acceptance import AcceptanceRepository
from app.database.repositories.good import GoodRepository
from app.database.repositories.sku import SkuRepository
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
