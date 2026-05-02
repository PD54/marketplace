from uuid import uuid7, UUID
from collections.abc import Callable

import pytest
from unittest.mock import AsyncMock, call

from app.models.product import ProductORM
from app.models.sku import SkuORM
from app.controllers.sku_controller import get_item_info
from app.pydantic_schemas.responses.get_item_info import GetItemInfoResponse
from app.exceptions.http_exceptions import NotFoundError
from tests.fixtures.model_objects_fabrics import product_fabric, sku_fabric


async def test_correct_response(
    sku_fabric: Callable[..., SkuORM],
    product_fabric: Callable[..., ProductORM]
):
    mock_session = AsyncMock()
    sku_of_product = sku_fabric()
    product_to_search = product_fabric(sku_id=sku_of_product.id)
    mock_session.get = AsyncMock(
        side_effect=[product_to_search, sku_of_product]
    )

    result = await get_item_info(id=product_to_search.id, database=mock_session)

    mock_session.get.assert_has_awaits(
        [
            call(ProductORM, product_to_search.id),
            call(SkuORM, product_to_search.sku_id)
        ]
    )
    assert mock_session.get.await_count == 2

    assert isinstance(result, GetItemInfoResponse)

    assert result.id == product_to_search.id
    assert result.sku_id == product_to_search.sku_id
    assert result.stock == product_to_search.stock
    assert result.reserved_state == product_to_search.reserved_state


async def test_product_not_found():
    mock_session = AsyncMock()
    id_to_search = uuid7()
    mock_session.get = AsyncMock(return_value=None)

    with pytest.raises(NotFoundError) as exception_info:
        await get_item_info(id=id_to_search, database=mock_session)

    mock_session.get.assert_awaited_once_with(ProductORM, id_to_search)

    assert exception_info.value.status_code == 404
    assert exception_info.value.detail == "Not found"


async def test_sku_of_product_not_found(
    product_fabric: Callable[..., ProductORM]
):
    mock_session = AsyncMock()
    product_to_search = product_fabric()
    mock_session.get = AsyncMock(side_effect=[product_to_search, None])

    with pytest.raises(NotFoundError) as exception_info:
        await get_item_info(id=product_to_search.id, database=mock_session)

    mock_session.get.assert_has_awaits(
        [
            call(ProductORM, product_to_search.id),
            call(SkuORM, product_to_search.sku_id)
        ]
    )
    assert mock_session.get.await_count == 2

    assert exception_info.value.status_code == 404
    assert exception_info.value.detail == "Sku of the product not found"
