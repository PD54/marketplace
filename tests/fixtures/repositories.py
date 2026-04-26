import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.repositories.product import ProductRepository
from app.database.repositories.sku import SkuRepository


@pytest.fixture
def product_repository(db_session: AsyncSession) -> ProductRepository:
    return ProductRepository(db_session)


@pytest.fixture
def sku_repository(db_session: AsyncSession) -> SkuRepository:
    return SkuRepository(db_session)
