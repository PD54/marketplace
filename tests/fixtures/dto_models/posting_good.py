from decimal import Decimal

import pytest

from app.database.dto.good import GoodDTO
from app.database.dto.posting_good import PostingGoodDTO
from app.database.dto.sku import SkuDTO


@pytest.fixture
def posting_good(
    posting: PostingGoodDTO,
    good_reserved: GoodDTO,
    sku: SkuDTO,
) -> PostingGoodDTO:
    return PostingGoodDTO(
        posting_id=posting.id,
        good_id=good_reserved.id,
        good_sku_id=sku.id,
        good_cost=Decimal("4000.00"),
        good_stock=good_reserved.stock,
    )
