from fastapi import Depends

from app.database.repositories.sku import SkuRepository
from app.dependencies.repositories import get_sku_repository
from app.services.sku.create_sku_service import CreateSkuService
from app.services.sku.toggle_is_hidden import ToggleIsHiddenService


def get_create_sku_service(
    sku_repo: SkuRepository = Depends(get_sku_repository),
) -> CreateSkuService:
    return CreateSkuService(sku_repo)


def get_toggle_is_hidden_service(
    sku_repo: SkuRepository = Depends(get_sku_repository),
) -> ToggleIsHiddenService:
    return ToggleIsHiddenService(sku_repo)
