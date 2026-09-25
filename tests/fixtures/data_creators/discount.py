import pytest

from app.database.dto.discount import DiscountDTO
from app.database.dto.sku import SkuDTO
from app.database.repositories.discount import DiscountRepository


@pytest.fixture
async def discount_active_in_db(
    discount_active: DiscountDTO,
    sku_in_db: SkuDTO,
    discount_repository: DiscountRepository,
) -> DiscountDTO:
    return await discount_repository.create(discount_active)


@pytest.fixture
async def discount_active_higher_percentage_in_db(
    discount_active_higher_percentage: DiscountDTO,
    sku_in_db: SkuDTO,
    discount_repository: DiscountRepository,
) -> DiscountDTO:
    return await discount_repository.create(discount_active_higher_percentage)


@pytest.fixture
async def discount_finished_highest_percentage_in_db(
    discount_finished_highest_percentage: DiscountDTO,
    sku_in_db: SkuDTO,
    discount_repository: DiscountRepository,
) -> DiscountDTO:
    return await discount_repository.create(
        discount_finished_highest_percentage,
    )


@pytest.fixture
async def discounts_list_in_db(
    discounts_list: list[DiscountDTO],
    sku_in_db: SkuDTO,
    discount_repository: DiscountRepository,
) -> list[DiscountDTO]:
    return await discount_repository.bulk_create(discounts_list)
