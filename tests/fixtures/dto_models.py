from decimal import Decimal

import pytest

from app.database.dto.product import ProductDTO 
from app.database.dto.sku import SkuDTO


@pytest.fixture
def product_dto(sku_dto: SkuDTO) -> ProductDTO:
    return ProductDTO(sku_id=sku_dto.id)


@pytest.fixture
def sku_dto() -> SkuDTO:
    return SkuDTO(base_price=Decimal("5000.00"))
