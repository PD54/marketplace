from fastapi import Depends

from app.database.repositories.discount import DiscountRepository
from app.database.repositories.good import GoodRepository
from app.database.repositories.sku import SkuRepository
from app.database.repositories.sku_and_discount import SkuAndDiscountRepository
from app.dependencies.repositories import (
    get_discount_repository,
    get_good_repository,
    get_sku_and_discount_repository,
    get_sku_repository,
)
from app.services.sku.create_sku_service import CreateSkuService
from app.services.sku.get_sku_info_service import GetSkuInfoService
from app.services.sku.set_sku_price_service import SetSkuPriceService
from app.services.sku.toggle_is_hidden_service import ToggleIsHiddenService


def get_create_sku_service(
    sku_repo: SkuRepository = Depends(get_sku_repository),
) -> CreateSkuService:
    return CreateSkuService(sku_repo=sku_repo)


def get_toggle_is_hidden_service(
    sku_repo: SkuRepository = Depends(get_sku_repository),
) -> ToggleIsHiddenService:
    return ToggleIsHiddenService(sku_repo=sku_repo)


def get_set_sku_price_service(
    sku_repo: SkuRepository = Depends(get_sku_repository),
) -> SetSkuPriceService:
    return SetSkuPriceService(sku_repo=sku_repo)


def get_get_sku_info_service(
    sku_repo: SkuRepository = Depends(get_sku_repository),
    discount_repo: DiscountRepository = Depends(get_discount_repository),
    sku_and_discount_repo: SkuAndDiscountRepository = Depends(
        get_sku_and_discount_repository,
    ),
    good_repo: GoodRepository = Depends(get_good_repository),
) -> GetSkuInfoService:
    return GetSkuInfoService(
        sku_repo=sku_repo,
        discount_repo=discount_repo,
        sku_and_discount_repo=sku_and_discount_repo,
        good_repo=good_repo,
    )
