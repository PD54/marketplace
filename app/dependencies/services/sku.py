from fastapi import Depends

from app.database.repositories.sku import SkuRepository
from app.dependencies.repositories import get_sku_repository
from app.services.sku.create_sku_service import CreateSkuService


def get_create_sku_service(
    sku_repo: SkuRepository = Depends(get_sku_repository),
) -> CreateSkuService:
    return CreateSkuService(sku_repo)
