from uuid import uuid7

from httpx import AsyncClient

from app.database.dto.product import ProductDTO
from app.services.product.dto.get_item_info import GetItemInfoResponse


async def test_get_item_info_success(
    client: AsyncClient,
    product_in_db: ProductDTO
):
    response = await client.get(f"/getItemInfo?id={product_in_db.id}")
    
    assert response.status_code == 200

    data = response.json()
    actual = GetItemInfoResponse.model_validate(data)
    expected = GetItemInfoResponse.model_validate(product_in_db)
    assert actual == expected


async def test_get_item_info_product_not_found(client: AsyncClient):
    random_id = uuid7()
    response = await client.get(f"/getItemInfo?id={random_id}")
    
    assert response.status_code == 404
    assert response.json()["detail"] == "Item not found"
