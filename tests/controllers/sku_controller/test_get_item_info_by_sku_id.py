from httpx import AsyncClient

from app.database.dto.good import GoodDTO
from app.database.dto.sku import SkuDTO
from app.services.good.dto.get_item_info_by_sku_id import (
    GetItemInfoBySkuIdItemOutputDTO,
    GetItemInfoBySkuIdOutputDTO,
)


async def test_happy_path(
    client: AsyncClient,
    sku_in_db: SkuDTO,
    goods_in_db: list[GoodDTO],
):
    response = await client.get(f"getItemInfoBySkuId?id={sku_in_db.id}")
    data = response.json()

    output_dto = GetItemInfoBySkuIdOutputDTO.model_validate(data)
    actual_list_of_goods = output_dto.items
    expected_list_of_goods = [
        GetItemInfoBySkuIdItemOutputDTO(
            item_id=good.id,
            stock=good.stock,
            reserved_state=good.reserved_state,
        )
        for good in goods_in_db
    ]

    actual_list_of_goods.sort(
        key=lambda good: (good.item_id, good.stock, good.reserved_state),
    )
    expected_list_of_goods.sort(
        key=lambda good: (good.item_id, good.stock, good.reserved_state),
    )

    assert response.status_code == 200

    assert actual_list_of_goods == expected_list_of_goods


async def test_no_goods_found_success(
    client: AsyncClient,
    sku_in_db: SkuDTO,
):
    response = await client.get(f"/getItemInfoBySkuId?id={sku_in_db.id}")
    data = response.json()
    output_dto = GetItemInfoBySkuIdOutputDTO.model_validate(data)
    actual_list_of_goods = output_dto.items

    assert response.status_code == 200

    assert actual_list_of_goods == []
