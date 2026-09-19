from decimal import Decimal
from uuid import uuid7

from httpx import AsyncClient

from app.database.dto.good import GoodDTO, GoodStock
from app.database.dto.posting_good import (
    PostingGoodCancelReason,
    PostingGoodDTO,
)
from app.database.dto.task import TaskDTO, TaskStatus
from app.database.repositories.good import GoodRepository
from app.database.repositories.posting_good import PostingGoodRepository
from app.database.repositories.task import TaskRepository
from app.services.good.dto.markdown_item import MarkdownItemInputDTO


async def test_happy_path(
    client: AsyncClient,
    good_reserved_in_db: GoodDTO,
    good_in_db: GoodDTO,
    posting_good_in_db: PostingGoodDTO,
    task_picking_in_work_in_db: TaskDTO,
    good_repository: GoodRepository,
    posting_good_repository: PostingGoodRepository,
    task_repository: TaskRepository,
):
    input_dto = MarkdownItemInputDTO(
        id=good_reserved_in_db.id,
        percentage=Decimal("30.00"),
    )
    request_data = input_dto.model_dump(mode="json")
    response = await client.post(url="/markdownItem", json=request_data)

    updated_good = await good_repository.get_by_id(
        good_reserved_in_db.id,
    )
    updated_posting_good = await posting_good_repository.get_by_id(
        posting_good_in_db.id,
    )
    updated_task = await task_repository.get_by_id(
        task_picking_in_work_in_db.id,
    )

    new_good_posting_goods = await posting_good_repository.get_by_good_id(
        good_in_db.id,
    )
    new_good_tasks = await task_repository.get_by_good_id(good_in_db.id)

    new_posting_good = new_good_posting_goods[0]
    new_task = new_good_tasks[0]

    assert response.status_code == 200

    assert updated_good.reserved_state is False
    assert updated_good.stock == GoodStock.defect
    assert updated_good.discount_percentage == input_dto.percentage

    assert (
        updated_posting_good.cancel_reason
        == PostingGoodCancelReason.good_defected
    )

    assert updated_task.status == TaskStatus.cancelled

    assert new_posting_good.good_id == good_in_db.id
    assert new_posting_good.posting_id == updated_posting_good.posting_id
    assert new_posting_good.good_stock == updated_posting_good.good_stock
    assert new_posting_good.good_sku_id == updated_posting_good.good_sku_id

    assert new_task.good_id == good_in_db.id
    assert new_task.posting_id == updated_posting_good.posting_id


async def test_success_without_new_good(
    client: AsyncClient,
    good_reserved_in_db: GoodDTO,
    posting_good_in_db: PostingGoodDTO,
    task_picking_in_work_in_db: TaskDTO,
    good_repository: GoodRepository,
    posting_good_repository: PostingGoodRepository,
    task_repository: TaskRepository,
):
    input_dto = MarkdownItemInputDTO(
        id=good_reserved_in_db.id,
        percentage=Decimal("30.00"),
    )
    request_data = input_dto.model_dump(mode="json")
    response = await client.post(url="/markdownItem", json=request_data)

    updated_good = await good_repository.get_by_id(
        good_reserved_in_db.id,
    )
    updated_posting_good = await posting_good_repository.get_by_id(
        posting_good_in_db.id,
    )
    updated_task = await task_repository.get_by_id(
        task_picking_in_work_in_db.id,
    )

    assert response.status_code == 200

    assert updated_good.reserved_state is False
    assert updated_good.stock == GoodStock.defect
    assert updated_good.discount_percentage == input_dto.percentage

    assert (
        updated_posting_good.cancel_reason
        == PostingGoodCancelReason.good_defected
    )

    assert updated_task.status == TaskStatus.cancelled


async def test_already_on_defect_stock(
    client: AsyncClient,
    good_with_defect_stock_in_db: GoodDTO,
    good_repository: GoodRepository,
):
    input_dto = MarkdownItemInputDTO(
        id=good_with_defect_stock_in_db.id,
        percentage=Decimal("30.00"),
    )
    request_data = input_dto.model_dump(mode="json")
    response = await client.post(url="/markdownItem", json=request_data)

    updated_good = await good_repository.get_by_id(input_dto.id)

    assert response.status_code == 200

    assert updated_good.stock == GoodStock.defect
    assert updated_good.discount_percentage == input_dto.percentage
    assert updated_good.updated_at > good_with_defect_stock_in_db.updated_at


async def test_good_not_found(
    client: AsyncClient,
):
    input_dto = MarkdownItemInputDTO(
        id=uuid7(),
        percentage=Decimal("30.00"),
    )
    request_data = input_dto.model_dump(mode="json")
    response = await client.post(url="/markdownItem", json=request_data)

    assert response.status_code == 404
    assert response.json()["detail"] == "Good not found"
