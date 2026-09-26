from decimal import Decimal
from uuid import uuid7

from httpx import AsyncClient

from app.database.dto.sku import SkuDTO
from app.database.repositories.discount import DiscountRepository
from app.database.repositories.sku_and_discount import SkuAndDiscountRepository
from app.services.discount.dto.create_discount import (
    CreateDiscountInputDTO,
    CreateDiscountOutputDTO,
)


async def test_happy_path(
    client: AsyncClient,
    sku_in_db: SkuDTO,
    discount_repository: DiscountRepository,
    sku_and_discount_repository: SkuAndDiscountRepository,
):
    input_dto = CreateDiscountInputDTO(
        sku_ids=[sku_in_db.id],
        percentage=Decimal("15.00"),
    )
    request_data = input_dto.model_dump(mode="json")
    response = await client.post(
        url="/createDiscount",
        json=request_data,
    )

    created_discount_from_response = CreateDiscountOutputDTO.model_validate(
        response.json()
    )
    created_discount_in_db = await discount_repository.get_by_id(
        created_discount_from_response.id
    )
    created_sku_and_discounts_in_db_list = (
        await sku_and_discount_repository.get_by_discount_id(
            created_discount_in_db.id
        )
    )
    created_sku_and_discount_in_db = created_sku_and_discounts_in_db_list[0]

    assert response.status_code == 200

    assert created_discount_in_db.percentage == input_dto.percentage

    assert len(created_sku_and_discounts_in_db_list) == 1
    assert created_sku_and_discount_in_db.sku_id == sku_in_db.id


async def test_multiple_skus_success(
    client: AsyncClient,
    sku_in_db: SkuDTO,
    sku_second_in_db: SkuDTO,
    discount_repository: DiscountRepository,
    sku_and_discount_repository: SkuAndDiscountRepository,
):
    input_dto = CreateDiscountInputDTO(
        sku_ids=[sku_in_db.id, sku_second_in_db.id],
        percentage=Decimal("15.00"),
    )
    request_data = input_dto.model_dump(mode="json")
    response = await client.post(
        url="/createDiscount",
        json=request_data,
    )

    created_discount_from_response = CreateDiscountOutputDTO.model_validate(
        response.json()
    )
    created_discount_in_db = await discount_repository.get_by_id(
        created_discount_from_response.id
    )
    created_sku_and_discounts_in_db_list = (
        await sku_and_discount_repository.get_by_discount_id(
            created_discount_in_db.id
        )
    )

    expected_sku_ids_list = [
        sku_and_discount.sku_id
        for sku_and_discount in created_sku_and_discounts_in_db_list
    ]
    expected_sku_ids_list.sort()

    assert response.status_code == 200

    assert created_discount_in_db.percentage == input_dto.percentage

    assert expected_sku_ids_list == sorted(input_dto.sku_ids)


async def test_non_existing_sku_id_in_input_dto(
    client: AsyncClient,
    sku_in_db: SkuDTO,
):
    input_dto = CreateDiscountInputDTO(
        sku_ids=[sku_in_db.id, uuid7()],
        percentage=Decimal("15.00"),
    )
    request_data = input_dto.model_dump(mode="json")
    response = await client.post(
        url="/createDiscount",
        json=request_data,
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Sku not found"


async def test_not_unique_sku_id_in_input_dto(
    client: AsyncClient,
    sku_in_db: SkuDTO,
):
    request_data = {
        "sku_ids": [str(sku_in_db.id), str(sku_in_db.id)],
        "percentage": "15.00",
    }
    response = await client.post(
        url="/createDiscount",
        json=request_data,
    )

    assert response.status_code == 422
    assert (
        response.json()["detail"][0]["msg"]
        == "Value error, SKU ids must be unique"
    )
