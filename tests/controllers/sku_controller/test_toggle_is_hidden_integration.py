from uuid import uuid7

from httpx import AsyncClient

from app.database.dto.sku import SkuDTO
from app.database.repositories.sku import SkuRepository
from app.services.sku.dto.toggle_is_hidden import ToggleIsHiddenInputDTO


async def test_toggle_is_hidden_success(
    sku_in_db: SkuDTO,
    client: AsyncClient,
    sku_repository: SkuRepository,
):
    toggle_is_hidden_input_dto = ToggleIsHiddenInputDTO(
        sku_id=sku_in_db.id,
        is_hidden=True,
    )
    request_data = toggle_is_hidden_input_dto.model_dump(mode="json")
    response = await client.post(
        url="/toggleIsHidden",
        json=request_data,
    )

    updated_sku = await sku_repository.get_by_id(sku_in_db.id)

    expected_is_hidden = toggle_is_hidden_input_dto.is_hidden
    actual_is_hidden = updated_sku.is_hidden

    previous_updated_at = sku_in_db.updated_at
    new_updated_at = updated_sku.updated_at

    assert response.status_code == 200
    assert expected_is_hidden == actual_is_hidden
    assert previous_updated_at != new_updated_at


async def test_toggle_is_hidden_sku_not_found(client: AsyncClient):
    toggle_is_hidden_input_dto = ToggleIsHiddenInputDTO(
        sku_id=uuid7(),
        is_hidden=True,
    )
    request_data = toggle_is_hidden_input_dto.model_dump(mode="json")
    response = await client.post(
        url="/toggleIsHidden",
        json=request_data,
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Sku not found"
