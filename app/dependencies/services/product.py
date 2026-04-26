from fastapi import Depends

from app.services.product.get_item_info_service import GetItemInfoService
from app.database.repositories.product import ProductRepository
from app.database.repositories.sku import SkuRepository
from app.dependencies.repositories import (
    get_product_repository,
    get_sku_repository
)


def get_get_item_info_service(
    product_repo: ProductRepository = Depends(get_product_repository),
    sku_repo: SkuRepository = Depends(get_sku_repository)
) -> GetItemInfoService:
    return GetItemInfoService(product_repo=product_repo, sku_repo=sku_repo)
