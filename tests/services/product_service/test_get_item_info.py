from uuid import uuid7

import pytest
from unittest.mock import AsyncMock

from app.database.dto.product import ProductDTO
from app.database.dto.sku import SkuDTO
from app.database.repositories.product import ProductRepository
from app.database.repositories.sku import SkuRepository
from app.services.product.get_item_info_service import GetItemInfoService
from app.services.product.exceptions import ItemNotFoundError
from app.services.sku.exceptions import SkuNotFoundError


@pytest.fixture
def get_item_info_service() -> GetItemInfoService:
    return GetItemInfoService(
        product_repo=AsyncMock(spec=ProductRepository),
        sku_repo=AsyncMock(spec=SkuRepository)
    )


async def test_correct_response(
    product_dto: ProductDTO,
    sku_dto: SkuDTO, 
    get_item_info_service: GetItemInfoService
):
    get_item_info_service.product_repo.get_by_id = AsyncMock(
        return_value=product_dto
    )
    get_item_info_service.sku_repo.get_by_id = AsyncMock(
        return_value=sku_dto
    )

    result = await get_item_info_service.get_item_info(
        product_id=product_dto.id
    )

    assert result.id == product_dto.id
    assert result.sku_id == product_dto.sku_id
    assert result.stock == product_dto.stock
    assert result.reserved_state == product_dto.reserved_state


async def test_product_not_found(
    get_item_info_service: GetItemInfoService
):
    id_to_search = uuid7()

    get_item_info_service.product_repo.get_by_id = AsyncMock(
        return_value=None
    )
    get_item_info_service.sku_repo.get_by_id = AsyncMock(
        return_value=None
    )

    with pytest.raises(ItemNotFoundError):
        await get_item_info_service.get_item_info(product_id=id_to_search)


async def test_sku_of_product_not_found(
    product_dto: ProductDTO, 
    get_item_info_service: GetItemInfoService
):
    get_item_info_service.product_repo.get_by_id = AsyncMock(
        return_value=product_dto
    )
    get_item_info_service.sku_repo.get_by_id = AsyncMock(
        return_value=None
    )

    with pytest.raises(SkuNotFoundError):
        await get_item_info_service.get_item_info(product_id=product_dto.id)
