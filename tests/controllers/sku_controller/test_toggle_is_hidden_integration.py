from uuid import uuid7

from httpx import AsyncClient

from app.database.dto.sku import SkuDTO
from app.database.repositories.sku import SkuRepository
from app.services.sku.dto.toggle_is_hidden import ToggleIsHiddenInputDTO


async def test_happy_path(
    sku_in_db: SkuDTO,
    client: AsyncClient,
    sku_repository: SkuRepository,
):
    input_dto = ToggleIsHiddenInputDTO(
        sku_id=sku_in_db.id,
        is_hidden=True,
    )
    request_data = input_dto.model_dump(mode="json")
    response = await client.post(
        url="/toggleIsHidden",
        json=request_data,
    )

    updated_sku = await sku_repository.get_by_id(sku_in_db.id)

    assert response.status_code == 200
    assert updated_sku.is_hidden is True
    assert updated_sku.updated_at > sku_in_db.updated_at


async def test_with_same_is_hidden_value_success(
    sku_in_db: SkuDTO,
    client: AsyncClient,
    sku_repository: SkuRepository,
):
    input_dto = ToggleIsHiddenInputDTO(
        sku_id=sku_in_db.id,
        is_hidden=sku_in_db.is_hidden,
    )
    request_data = input_dto.model_dump(mode="json")
    response = await client.post(
        url="/toggleIsHidden",
        json=request_data,
    )

    current_sku = await sku_repository.get_by_id(sku_in_db.id)

    assert response.status_code == 200
    assert sku_in_db.updated_at == current_sku.updated_at
    assert sku_in_db.is_hidden == current_sku.is_hidden


async def test_sku_not_found_error(client: AsyncClient):
    input_dto = ToggleIsHiddenInputDTO(
        sku_id=uuid7(),
        is_hidden=True,
    )
    request_data = input_dto.model_dump(mode="json")
    response = await client.post(
        url="/toggleIsHidden",
        json=request_data,
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Sku not found"
