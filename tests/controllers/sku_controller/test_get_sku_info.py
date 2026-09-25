from decimal import Decimal
from uuid import uuid7

from httpx import AsyncClient

from app.database.dto.discount import DiscountDTO
from app.database.dto.good import GoodDTO
from app.database.dto.sku import SkuDTO
from app.database.dto.sku_and_discount import SkuAndDiscountDTO
from app.services.sku.dto.get_sku_info import GetSkuInfoOutputDTO


async def test_happy_path(
    client: AsyncClient,
    sku_in_db: SkuDTO,
    goods_list_in_db: list[GoodDTO],
    discount_active_in_db: DiscountDTO,
    sku_and_discount_active_in_db: SkuAndDiscountDTO,
):
    response = await client.get(f"/getSkuInfo?id={sku_in_db.id}")
    data = response.json()
    output_dto = GetSkuInfoOutputDTO.model_validate(data)

    assert response.status_code == 200

    assert output_dto.id == sku_in_db.id
    assert output_dto.created_at == sku_in_db.created_at
    assert output_dto.actual_price == Decimal("4000")
    assert output_dto.base_price == sku_in_db.base_price
    assert output_dto.count == len(goods_list_in_db)
    assert output_dto.is_hidden == sku_in_db.is_hidden


async def test_many_discounts_success(
    client: AsyncClient,
    sku_in_db: SkuDTO,
    discounts_list_in_db: list[DiscountDTO],
    sku_and_discounts_list_in_db: list[SkuAndDiscountDTO],
):
    response = await client.get(f"/getSkuInfo?id={sku_in_db.id}")
    data = response.json()
    output_dto = GetSkuInfoOutputDTO.model_validate(data)

    assert response.status_code == 200

    assert output_dto.id == sku_in_db.id
    assert output_dto.actual_price == Decimal("3750")


async def test_no_active_discounts_success(
    client: AsyncClient,
    sku_in_db: SkuDTO,
    discount_finished_highest_percentage_in_db: DiscountDTO,
    sku_and_discount_finished_highest_percentage_in_db: SkuAndDiscountDTO,
):
    response = await client.get(f"/getSkuInfo?id={sku_in_db.id}")
    data = response.json()
    output_dto = GetSkuInfoOutputDTO.model_validate(data)

    assert response.status_code == 200

    assert output_dto.id == sku_in_db.id
    assert output_dto.actual_price == sku_in_db.base_price


async def test_no_goods_success(
    client: AsyncClient,
    sku_in_db: SkuDTO,
):
    response = await client.get(f"/getSkuInfo?id={sku_in_db.id}")
    data = response.json()
    output_dto = GetSkuInfoOutputDTO.model_validate(data)

    assert response.status_code == 200

    assert output_dto.id == sku_in_db.id
    assert output_dto.count == 0


async def test_sku_not_found(client: AsyncClient):
    response = await client.get(f"/getSkuInfo?id={uuid7()}")

    assert response.status_code == 404
    assert response.json()["detail"] == "Sku not found"
