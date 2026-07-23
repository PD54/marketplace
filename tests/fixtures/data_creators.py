import pytest

from app.database.dto.product import ProductDTO
from app.database.dto.sku import SkuDTO
from app.database.repositories.product import ProductRepository
from app.database.repositories.sku import SkuRepository


@pytest.fixture
async def sku_in_db(
    sku_repository: SkuRepository,
    sku_dto: SkuDTO
) -> SkuDTO:
    return await sku_repository.create(sku_dto)


@pytest.fixture
async def product_in_db(
    product_repository: ProductRepository,
    product_dto: ProductDTO,
    sku_in_db: SkuDTO
) -> ProductDTO:
    return await product_repository.create(product_dto)
