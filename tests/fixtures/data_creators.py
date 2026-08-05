import pytest

from app.database.dto.good import GoodDTO
from app.database.dto.sku import SkuDTO
from app.database.repositories.good import GoodRepository
from app.database.repositories.sku import SkuRepository


@pytest.fixture
async def sku_in_db(
    sku_repository: SkuRepository,
    sku_dto: SkuDTO
) -> SkuDTO:
    return await sku_repository.create(sku_dto)


@pytest.fixture
async def good_in_db(
    good_repository: GoodRepository,
    good_dto: GoodDTO,
    sku_in_db: SkuDTO
) -> GoodDTO:
    return await good_repository.create(good_dto)
