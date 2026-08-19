from decimal import Decimal

import pytest

from app.database.dto.good import GoodDTO
from app.database.dto.sku import SkuDTO


@pytest.fixture
def good_dto(sku_dto: SkuDTO) -> GoodDTO:
    return GoodDTO(sku_id=sku_dto.id)


@pytest.fixture
def sku_dto() -> SkuDTO:
    return SkuDTO(base_price=Decimal("5000.00"))
