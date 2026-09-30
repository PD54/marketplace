from uuid import uuid7

from httpx import AsyncClient

from app.database.dto.discount import DiscountDTO, DiscountStatus
from app.database.repositories.discount import DiscountRepository
from app.services.discount.dto.cancel_discount import CancelDiscountInputDTO


async def test_happy_path(
    client: AsyncClient,
    discount_active_in_db: DiscountDTO,
    discount_repository: DiscountRepository,
):
    input_dto = CancelDiscountInputDTO(
        id=discount_active_in_db.id,
    )
    request_data = input_dto.model_dump(mode="json")
    response = await client.post(
        url="/cancelDiscount",
        json=request_data,
    )

    updated_discount = await discount_repository.get_by_id(
        discount_active_in_db.id,
    )

    assert response.status_code == 200

    assert updated_discount.status == DiscountStatus.finished
    assert updated_discount.updated_at > discount_active_in_db.updated_at


async def test_discount_already_finished_success(
    client: AsyncClient,
    discount_finished_highest_percentage_in_db: DiscountDTO,
    discount_repository: DiscountRepository,
):
    input_dto = CancelDiscountInputDTO(
        id=discount_finished_highest_percentage_in_db.id,
    )
    request_data = input_dto.model_dump(mode="json")
    response = await client.post(
        url="/cancelDiscount",
        json=request_data,
    )

    current_discount = await discount_repository.get_by_id(
        discount_finished_highest_percentage_in_db.id,
    )

    assert response.status_code == 200

    assert (
        current_discount.updated_at
        == discount_finished_highest_percentage_in_db.updated_at
    )
    assert (
        current_discount.status
        == discount_finished_highest_percentage_in_db.status
    )


async def test_discount_not_found(
    client: AsyncClient,
):
    input_dto = CancelDiscountInputDTO(
        id=uuid7(),
    )
    request_data = input_dto.model_dump(mode="json")
    response = await client.post(
        url="/cancelDiscount",
        json=request_data,
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Discount not found"
