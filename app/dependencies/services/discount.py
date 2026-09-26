from fastapi import Depends

from app.database.repositories.discount import DiscountRepository
from app.database.repositories.sku import SkuRepository
from app.database.repositories.sku_and_discount import SkuAndDiscountRepository
from app.dependencies.repositories import (
    get_discount_repository,
    get_sku_and_discount_repository,
    get_sku_repository,
)
from app.services.discount.create_discount_service import CreateDiscountService


def get_create_discount_service(
    sku_repo: SkuRepository = Depends(get_sku_repository),
    discount_repo: DiscountRepository = Depends(get_discount_repository),
    sku_and_discount_repo: SkuAndDiscountRepository = Depends(
        get_sku_and_discount_repository,
    ),
) -> CreateDiscountService:
    return CreateDiscountService(
        sku_repo=sku_repo,
        discount_repo=discount_repo,
        sku_and_discount_repo=sku_and_discount_repo,
    )
