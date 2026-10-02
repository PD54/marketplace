from uuid import uuid7

from httpx import AsyncClient

from app.database.dto.discount import DiscountDTO
from app.database.dto.sku_and_discount import SkuAndDiscountDTO
from app.services.discount.dto.get_discount import GetDiscountOutputDTO


async def test_happy_path(
    client: AsyncClient,
    discount_active_in_db: DiscountDTO,
    sku_and_discount_active_in_db: SkuAndDiscountDTO,
):
    response = await client.get(f"/getDiscount?id={discount_active_in_db.id}")
    data = response.json()
    output_dto = GetDiscountOutputDTO.model_validate(data)

    assert response.status_code == 200

    assert output_dto.id == discount_active_in_db.id
    assert output_dto.status == discount_active_in_db.status
    assert output_dto.created_at == discount_active_in_db.created_at
    assert output_dto.percentage == discount_active_in_db.percentage

    assert len(output_dto.sku_ids) == 1
    assert output_dto.sku_ids == [sku_and_discount_active_in_db.sku_id]


async def test_discount_without_sku_success(
    client: AsyncClient,
    discount_active_in_db: DiscountDTO,
):
    response = await client.get(f"/getDiscount?id={discount_active_in_db.id}")
    data = response.json()
    output_dto = GetDiscountOutputDTO.model_validate(data)

    assert response.status_code == 200

    assert output_dto.id == discount_active_in_db.id

    assert output_dto.sku_ids == []


async def test_discount_with_multiple_sku_success(
    client: AsyncClient,
    discount_active_in_db: DiscountDTO,
    sku_and_discount_with_many_sku_list_in_db: list[SkuAndDiscountDTO],
):
    response = await client.get(f"/getDiscount?id={discount_active_in_db.id}")
    data = response.json()
    output_dto = GetDiscountOutputDTO.model_validate(data)

    expected_sku_ids = [
        sku_and_discount.sku_id
        for sku_and_discount in sku_and_discount_with_many_sku_list_in_db
    ]

    assert response.status_code == 200

    assert output_dto.id == discount_active_in_db.id

    assert len(output_dto.sku_ids) == len(expected_sku_ids)
    assert set(output_dto.sku_ids) == set(expected_sku_ids)


async def test_discount_not_found(
    client: AsyncClient,
):
    response = await client.get(f"/getDiscount?id={uuid7()}")

    assert response.status_code == 404
    assert response.json()["detail"] == "Discount not found"
