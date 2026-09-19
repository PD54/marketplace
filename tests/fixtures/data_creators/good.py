import pytest

from app.database.dto.good import GoodDTO
from app.database.dto.sku import SkuDTO
from app.database.repositories.good import GoodRepository


@pytest.fixture
async def good_in_db(
    good_repository: GoodRepository,
    good: GoodDTO,
    sku_in_db: SkuDTO,
) -> GoodDTO:
    return await good_repository.create(good)


@pytest.fixture
async def good_reserved_in_db(
    good_repository: GoodRepository,
    good_reserved: GoodDTO,
    sku_in_db: SkuDTO,
) -> GoodDTO:
    return await good_repository.create(good_reserved)


@pytest.fixture
async def good_with_not_found_stock_in_db(
    good_repository: GoodRepository,
    good_with_not_found_stock: GoodDTO,
    sku_in_db: SkuDTO,
) -> GoodDTO:
    return await good_repository.create(good_with_not_found_stock)


@pytest.fixture
async def good_with_defect_stock_in_db(
    good_repository: GoodRepository,
    good_with_defect_stock: GoodDTO,
    sku_in_db: SkuDTO,
) -> GoodDTO:
    return await good_repository.create(good_with_defect_stock)


@pytest.fixture
async def goods_in_db(
    good_repository: GoodRepository,
    goods: list[GoodDTO],
    sku_in_db: SkuDTO,
) -> list[GoodDTO]:
    return await good_repository.bulk_create(goods)
