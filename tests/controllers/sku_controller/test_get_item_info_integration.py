from uuid import uuid7

from httpx import AsyncClient

from app.database.dto.good import GoodDTO
from app.services.good.dto.get_item_info import GetItemInfoOutputDTO


async def test_get_item_info_success(
    client: AsyncClient,
    good_in_db: GoodDTO,
):
    response = await client.get(f"/getItemInfo?id={good_in_db.id}")

    assert response.status_code == 200

    data = response.json()
    actual = GetItemInfoOutputDTO.model_validate(data)
    expected = GetItemInfoOutputDTO.model_validate(good_in_db)
    assert actual == expected


async def test_get_item_info_good_not_found(client: AsyncClient):
    random_id = uuid7()
    response = await client.get(f"/getItemInfo?id={random_id}")

    assert response.status_code == 404
    assert response.json()["detail"] == "Good not found"
