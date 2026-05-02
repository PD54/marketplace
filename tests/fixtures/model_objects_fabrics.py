from uuid import UUID, uuid7
from decimal import Decimal
from collections.abc import Callable

import pytest

from app.models.product import ProductORM
from app.models.sku import SkuORM


@pytest.fixture
def product_fabric() -> Callable[..., ProductORM]:
    def create_product(
        id: UUID | None = None,
        sku_id: UUID | None = None,
        stock: str = "not_found",
        reserved_state: bool = False
    ) -> ProductORM:
        return (
            ProductORM(
                id=id or uuid7(),
                sku_id=sku_id or uuid7(),
                stock=stock,
                reserved_state=reserved_state
            )
        )
    return create_product


@pytest.fixture
def sku_fabric() -> Callable[..., SkuORM]:
    def create_sku(
            id: UUID | None = None,
            base_price: Decimal | None = None,
            is_hidden: bool = False
    ) -> SkuORM:
        return (
            SkuORM(
                id=id or uuid7(),
                base_price=base_price or Decimal("0.0"),
                is_hidden=is_hidden
            )
        )
    return create_sku
