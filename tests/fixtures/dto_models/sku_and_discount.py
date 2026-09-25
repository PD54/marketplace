import pytest

from app.database.dto.sku import SkuDTO
from app.database.dto.sku_and_discount import SkuAndDiscountDTO


@pytest.fixture
def sku_and_discount_active(
    discount_active: SkuAndDiscountDTO,
    sku: SkuDTO,
) -> SkuAndDiscountDTO:
    return SkuAndDiscountDTO(
        discount_id=discount_active.id,
        sku_id=sku.id,
    )


@pytest.fixture
def sku_and_discount_active_higher_percentage(
    discount_active_higher_percentage: SkuAndDiscountDTO,
    sku: SkuDTO,
) -> SkuAndDiscountDTO:
    return SkuAndDiscountDTO(
        discount_id=discount_active_higher_percentage.id,
        sku_id=sku.id,
    )


@pytest.fixture
def sku_and_discount_finished_highest_percentage(
    discount_finished_highest_percentage: SkuAndDiscountDTO,
    sku: SkuDTO,
) -> SkuAndDiscountDTO:
    return SkuAndDiscountDTO(
        discount_id=discount_finished_highest_percentage.id,
        sku_id=sku.id,
    )


@pytest.fixture
def sku_and_discounts_list(
    sku_and_discount_active: SkuAndDiscountDTO,
    sku_and_discount_active_higher_percentage: SkuAndDiscountDTO,
    sku_and_discount_finished_highest_percentage: SkuAndDiscountDTO,
) -> list[SkuAndDiscountDTO]:
    return [
        sku_and_discount_active,
        sku_and_discount_active_higher_percentage,
        sku_and_discount_finished_highest_percentage,
    ]
