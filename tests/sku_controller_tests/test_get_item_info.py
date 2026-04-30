from uuid import uuid7

import pytest
from pytest_mock import MockerFixture

from app.models.product import Product
from app.controllers.sku_controller import get_item_info
from app.pydantic_schemas.responses.get_item_info import GetItemInfoResponse
from app.exceptions.http_exceptions import NotFound


@pytest.mark.asyncio
async def test_get_item_info_positive(mocker: MockerFixture) -> None:
    mock_session = mocker.AsyncMock()
    id = uuid7()
    product_to_search = Product(
        id=id,
        sku_id=uuid7(),
        stock="valid",
        reserved_state=False
    )
    mock_session.get = mocker.AsyncMock(return_value=product_to_search)

    result = await get_item_info(id=id, database=mock_session)

    mock_session.get.assert_awaited_once_with(Product, id)
    
    assert isinstance(result, GetItemInfoResponse)

    assert result.id == product_to_search.id
    assert result.sku_id == product_to_search.sku_id
    assert result.stock == product_to_search.stock
    assert result.reserved_state == product_to_search.reserved_state



@pytest.mark.asyncio
async def test_get_item_info_negative(mocker: MockerFixture) -> None:
    mock_session = mocker.AsyncMock()
    id_to_search = uuid7()
    mock_session.get = mocker.AsyncMock(return_value=None)

    with pytest.raises(NotFound) as exception_info:
        await get_item_info(id=id_to_search, database=mock_session)

    mock_session.get.assert_awaited_once_with(Product, id_to_search)

    assert exception_info.value.status_code == 404
    assert exception_info.value.detail == "Not found"
