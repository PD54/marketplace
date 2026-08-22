from unittest.mock import AsyncMock
from uuid import uuid7

import pytest

from app.database.dto.good import GoodDTO
from app.database.dto.sku import SkuDTO
from app.database.repositories.good import GoodRepository
from app.database.repositories.sku import SkuRepository
from app.services.good.exceptions import ItemNotFoundError
from app.services.good.get_item_info_service import GetItemInfoService
from app.services.sku.exceptions import SkuNotFoundError


@pytest.fixture
def get_item_info_service() -> GetItemInfoService:
    return GetItemInfoService(
        good_repo=AsyncMock(spec=GoodRepository),
        sku_repo=AsyncMock(spec=SkuRepository),
    )


async def test_correct_response(
    good_dto: GoodDTO,
    sku_dto: SkuDTO,
    get_item_info_service: GetItemInfoService,
):
    get_item_info_service.good_repo.get_by_id = AsyncMock(
        return_value=good_dto,
    )
    get_item_info_service.sku_repo.get_by_id = AsyncMock(
        return_value=sku_dto,
    )

    result = await get_item_info_service.get_item_info(
        good_id=good_dto.id,
    )

    assert result.id == good_dto.id
    assert result.sku_id == good_dto.sku_id
    assert result.stock == good_dto.stock
    assert result.reserved_state == good_dto.reserved_state


async def test_good_not_found(
    get_item_info_service: GetItemInfoService,
):
    id_to_search = uuid7()

    get_item_info_service.good_repo.get_by_id = AsyncMock(
        return_value=None,
    )
    get_item_info_service.sku_repo.get_by_id = AsyncMock(
        return_value=None,
    )

    with pytest.raises(ItemNotFoundError):
        await get_item_info_service.get_item_info(good_id=id_to_search)


async def test_sku_of_good_not_found(
    good_dto: GoodDTO,
    get_item_info_service: GetItemInfoService,
):
    get_item_info_service.good_repo.get_by_id = AsyncMock(
        return_value=good_dto,
    )
    get_item_info_service.sku_repo.get_by_id = AsyncMock(
        return_value=None,
    )

    with pytest.raises(SkuNotFoundError):
        await get_item_info_service.get_item_info(good_id=good_dto.id)
