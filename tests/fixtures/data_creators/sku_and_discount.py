import pytest

from app.database.dto.sku import SkuDTO
from app.database.dto.sku_and_discount import SkuAndDiscountDTO
from app.database.repositories.sku_and_discount import SkuAndDiscountRepository


@pytest.fixture
async def sku_and_discount_active_in_db(
    sku_and_discount_active: SkuAndDiscountDTO,
    sku_in_db: SkuDTO,
    sku_and_discount_repository: SkuAndDiscountRepository,
) -> SkuAndDiscountDTO:
    return await sku_and_discount_repository.create(sku_and_discount_active)


@pytest.fixture
async def sku_and_discount_active_higher_percentage_in_db(
    sku_and_discount_active_higher_percentage: SkuAndDiscountDTO,
    sku_in_db: SkuDTO,
    sku_and_discount_repository: SkuAndDiscountRepository,
) -> SkuAndDiscountDTO:
    return await sku_and_discount_repository.create(
        sku_and_discount_active_higher_percentage,
    )


@pytest.fixture
async def sku_and_discount_finished_highest_percentage_in_db(
    sku_and_discount_finished_highest_percentage: SkuAndDiscountDTO,
    sku_in_db: SkuDTO,
    sku_and_discount_repository: SkuAndDiscountRepository,
) -> SkuAndDiscountDTO:
    return await sku_and_discount_repository.create(
        sku_and_discount_finished_highest_percentage,
    )


@pytest.fixture
async def sku_and_discounts_list_in_db(
    sku_and_discounts_list: list[SkuAndDiscountDTO],
    sku_in_db: SkuDTO,
    sku_and_discount_repository: SkuAndDiscountRepository,
) -> list[SkuAndDiscountDTO]:
    return await sku_and_discount_repository.bulk_create(
        sku_and_discounts_list
    )
