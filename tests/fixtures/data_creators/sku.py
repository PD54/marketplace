import pytest

from app.database.dto.sku import SkuDTO
from app.database.repositories.sku import SkuRepository


@pytest.fixture
async def sku_in_db(
    sku_repository: SkuRepository,
    sku: SkuDTO,
) -> SkuDTO:
    return await sku_repository.create(sku)
