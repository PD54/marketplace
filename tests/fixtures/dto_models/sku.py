from decimal import Decimal

import pytest

from app.database.dto.sku import SkuDTO


@pytest.fixture
def sku() -> SkuDTO:
    return SkuDTO(base_price=Decimal("5000.00"))


@pytest.fixture
def sku_second() -> SkuDTO:
    return SkuDTO(base_price=Decimal("3000.00"))
