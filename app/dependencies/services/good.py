from fastapi import Depends

from app.database.repositories.good import GoodRepository
from app.database.repositories.sku import SkuRepository
from app.dependencies.repositories import (
    get_good_repository,
    get_sku_repository,
)
from app.services.good.get_item_info_service import GetItemInfoService


def get_get_item_info_service(
    good_repo: GoodRepository = Depends(get_good_repository),
    sku_repo: SkuRepository = Depends(get_sku_repository),
) -> GetItemInfoService:
    return GetItemInfoService(good_repo=good_repo, sku_repo=sku_repo)
