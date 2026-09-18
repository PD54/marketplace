from decimal import Decimal
from uuid import uuid7

from httpx import AsyncClient

from app.database.dto.sku import SkuDTO
from app.database.repositories.sku import SkuRepository
from app.services.sku.dto.set_sku_price import SetSkuPriceInputDTO


async def test_happy_path(
    sku_in_db: SkuDTO,
    client: AsyncClient,
    sku_repository: SkuRepository,
):
    input_dto = SetSkuPriceInputDTO(
        sku_id=sku_in_db.id,
        base_price=Decimal("25.00"),
    )
    request_data = input_dto.model_dump(mode="json")
    response = await client.post(
        url="/setSkuPrice",
        json=request_data,
    )

    updated_sku = await sku_repository.get_by_id(sku_in_db.id)

    assert response.status_code == 200
    assert updated_sku.base_price == input_dto.base_price
    assert updated_sku.updated_at > sku_in_db.updated_at


async def test_sku_not_found(client: AsyncClient):
    input_dto = SetSkuPriceInputDTO(
        sku_id=uuid7(),
        base_price=Decimal("25.00"),
    )
    request_data = input_dto.model_dump(mode="json")
    response = await client.post(
        url="/setSkuPrice",
        json=request_data,
    )

    assert response.status_code == 404, response.json()
    assert response.json()["detail"] == "Sku not found"
