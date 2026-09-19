from decimal import Decimal

import pytest

from app.database.dto.good import GoodDTO, GoodStock
from app.database.dto.sku import SkuDTO


@pytest.fixture
def good(sku: SkuDTO) -> GoodDTO:
    return GoodDTO(sku_id=sku.id)


@pytest.fixture
def good_reserved(sku: SkuDTO) -> GoodDTO:
    return GoodDTO(
        sku_id=sku.id,
        reserved_state=True,
    )


@pytest.fixture
def good_with_not_found_stock(sku: SkuDTO) -> GoodDTO:
    return GoodDTO(
        sku_id=sku.id,
        stock=GoodStock.not_found,
    )


@pytest.fixture
def good_with_defect_stock(sku: SkuDTO) -> GoodDTO:
    return GoodDTO(
        sku_id=sku.id,
        stock=GoodStock.defect,
        discount_percentage=Decimal("15.00"),
    )


@pytest.fixture
def goods(
    good: GoodDTO,
    good_reserved: GoodDTO,
    good_with_not_found_stock: GoodDTO,
    good_with_defect_stock: GoodDTO,
) -> list[GoodDTO]:
    return [
        good,
        good_reserved,
        good_with_not_found_stock,
        good_with_defect_stock,
    ]
