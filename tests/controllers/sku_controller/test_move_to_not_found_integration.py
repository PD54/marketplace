from uuid import uuid7

import pytest
from httpx import AsyncClient

from app.database.dto.good import GoodDTO, GoodStock
from app.database.dto.posting_good import PostingGoodDTO
from app.database.dto.sku import SkuDTO
from app.database.dto.task import TaskStatus
from app.database.repositories.good import GoodRepository
from app.database.repositories.posting_good import PostingGoodRepository
from app.database.repositories.task import TaskRepository
from app.services.good.dto.move_to_not_found import MoveToNotFoundInputDTO


@pytest.fixture
async def good_with_not_found_stock_in_db(
    good: GoodDTO,
    sku_in_db: SkuDTO,
    good_repository: GoodRepository,
) -> GoodDTO:
    return await good_repository.create(
        good.model_copy(update={"stock": GoodStock.not_found})
    )


async def test_move_to_not_found_success(
    client: AsyncClient,
    reserved_good_in_db: GoodDTO,
    posting_good_in_db: PostingGoodDTO,
    tasks_from_posting_in_db: TaskRepository,
    good_repository: GoodRepository,
    posting_good_repository: PostingGoodRepository,
    task_repository: TaskRepository,
):
    input_dto = MoveToNotFoundInputDTO(id=reserved_good_in_db.id)
    request_data = input_dto.model_dump(mode="json")
    response = await client.post(url="/moveToNotFound", json=request_data)

    updated_good = await good_repository.get_by_id(
        reserved_good_in_db.id,
    )
    updated_posting_goods_list = await posting_good_repository.get_by_good_id(
        reserved_good_in_db.id,
    )
    updated_tasks_list = await task_repository.get_by_good_id(
        reserved_good_in_db.id,
    )

    assert response.status_code == 200

    assert updated_good.reserved_state is False
    assert updated_good.stock == GoodStock.not_found

    for posting_good in updated_posting_goods_list:
        assert posting_good.cancel_reason

    for task in updated_tasks_list:
        assert task.status != TaskStatus.in_work


async def test_move_to_not_found_good_not_found_error(
    client: AsyncClient,
):
    input_dto = MoveToNotFoundInputDTO(id=uuid7())
    request_data = input_dto.model_dump(mode="json")
    response = await client.post(url="/moveToNotFound", json=request_data)

    assert response.status_code == 404
    assert response.json()["detail"] == "Good not found"


async def test_move_to_not_found_already_on_not_found_stock(
    client: AsyncClient,
    good_with_not_found_stock_in_db: GoodDTO,
):
    input_dto = MoveToNotFoundInputDTO(
        id=good_with_not_found_stock_in_db.id,
    )
    request_data = input_dto.model_dump(mode="json")
    response = await client.post(url="/moveToNotFound", json=request_data)

    assert response.status_code == 400
    assert response.json()["detail"] == "Good is already on not_found stock"
