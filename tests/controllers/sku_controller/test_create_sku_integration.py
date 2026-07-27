from httpx import AsyncClient

from app.database.dto.sku import SkuDTO
from app.database.repositories.sku import SkuRepository
from app.services.sku.dto.create_sku import (
    CreateSkuInputDTO,
    CreateSkuOutputDTO
)


async def test_create_sku_success(
    client: AsyncClient,
    sku_dto: SkuDTO,
    sku_repository: SkuRepository
):
    sku_to_create = CreateSkuInputDTO.model_validate(sku_dto)
    request_data = sku_to_create.model_dump(mode="json")
    response = await client.post(
        url="/createSku",
        json=request_data
    )

    assert response.status_code == 200

    data = response.json()
    created_sku_from_response = CreateSkuOutputDTO.model_validate(data)
    created_sku_in_db = await sku_repository.get_by_id(sku_to_create.id)

    assert created_sku_from_response.id == sku_to_create.id
    assert created_sku_from_response.base_price == sku_to_create.base_price
    assert created_sku_from_response.is_hidden == sku_to_create.is_hidden

    assert created_sku_in_db is not None
    assert created_sku_in_db.id == sku_to_create.id
    assert created_sku_in_db.base_price == sku_to_create.base_price
    assert created_sku_in_db.is_hidden == sku_to_create.is_hidden


async def test_create_sku_already_exists(
    client: AsyncClient,
    sku_in_db: SkuDTO
):
    existing_in_db_sku = CreateSkuInputDTO.model_validate(sku_in_db)
    request_data = existing_in_db_sku.model_dump(mode="json")

    response = await client.post(
        url="/createSku",
        json=request_data
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Sku with provided id already exists"
