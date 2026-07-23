from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies.session_generator import get_db
from app.database.repositories.product import ProductRepository
from app.database.repositories.sku import SkuRepository


def get_product_repository(
    database: AsyncSession = Depends(get_db)
) -> ProductRepository:
    return ProductRepository(database=database)


def get_sku_repository(
    database: AsyncSession = Depends(get_db)
) -> SkuRepository:
    return SkuRepository(database=database)