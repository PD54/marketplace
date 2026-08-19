from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.repositories.acceptance import AcceptanceRepository
from app.database.repositories.good import GoodRepository
from app.database.repositories.sku import SkuRepository
from app.database.repositories.task import TaskRepository
from app.dependencies.session_generator import get_db


def get_good_repository(
    database: AsyncSession = Depends(get_db),
) -> GoodRepository:
    return GoodRepository(database=database)


def get_sku_repository(
    database: AsyncSession = Depends(get_db),
) -> SkuRepository:
    return SkuRepository(database=database)


def get_task_repository(
    database: AsyncSession = Depends(get_db),
) -> TaskRepository:
    return TaskRepository(database=database)


def get_acceptance_repository(
    database: AsyncSession = Depends(get_db),
) -> AcceptanceRepository:
    return AcceptanceRepository(database=database)
