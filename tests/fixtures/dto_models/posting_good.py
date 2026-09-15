from decimal import Decimal

import pytest

from app.database.dto.good import GoodDTO
from app.database.dto.posting_good import PostingGoodDTO
from app.database.dto.sku import SkuDTO


@pytest.fixture
def posting_good(
    posting: PostingGoodDTO,
    reserved_good: GoodDTO,
    sku: SkuDTO,
) -> PostingGoodDTO:
    return PostingGoodDTO(
        posting_id=posting.id,
        good_id=reserved_good.id,
        good_sku_id=sku.id,
        good_cost=Decimal("4000.00"),
        good_stock=reserved_good.stock,
    )
