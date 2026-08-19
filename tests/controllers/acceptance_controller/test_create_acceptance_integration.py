from uuid import uuid7

import pytest
from httpx import AsyncClient

from app.database.dto.acceptance import AcceptanceDTO
from app.database.dto.good import GoodStock
from app.database.dto.sku import SkuDTO
from app.database.dto.task import TaskType, TaskDTO
from app.database.repositories.acceptance import AcceptanceRepository
from app.database.repositories.task import TaskRepository
from app.services.acceptance.dto.create_acceptance import (
    CreateAcceptanceInputDTO,
    CreateAcceptanceItemInputDTO,
    CreateAcceptanceOutputDTO
)


@pytest.fixture
def create_acceptance_item_input_dto() -> CreateAcceptanceItemInputDTO:
    return CreateAcceptanceItemInputDTO(
        sku_id=uuid7(),
        stock=GoodStock.valid,
        count=100
    )


async def send_request_return_output_dto(
    client: AsyncClient,
    items_to_accept: list[CreateAcceptanceItemInputDTO],
) -> CreateAcceptanceOutputDTO:
    create_acceptance_input_dto = CreateAcceptanceInputDTO(
        items_to_accept=items_to_accept
    )
    request_data = create_acceptance_input_dto.model_dump(mode="json")
    response = await client.post(
        url="createAcceptance",
        json=request_data
    )

    created_acceptance_from_response = (
        CreateAcceptanceOutputDTO.model_validate(response.json())
    )

    return created_acceptance_from_response


async def test_create_acceptance_non_existing_sku_success(
    client: AsyncClient,
    acceptance_repository: AcceptanceRepository,
    task_repository: TaskRepository,
    create_acceptance_item_input_dto: CreateAcceptanceItemInputDTO,
):
    items_to_accept = [create_acceptance_item_input_dto]

    created_acceptance_from_response = await send_request_return_output_dto(
        client=client,
        items_to_accept=items_to_accept
    )

    created_acceptance_in_db = await acceptance_repository.get_by_id(
        created_acceptance_from_response.id
    )

    created_tasks_in_db = await task_repository.get_by_acceptance_id(
        created_acceptance_in_db.id
    )

    task = created_tasks_in_db[0]

    assert len(created_tasks_in_db) == len(items_to_accept)

    assert task.sku_id == create_acceptance_item_input_dto.sku_id
    assert task.stock == create_acceptance_item_input_dto.stock
    assert task.count == create_acceptance_item_input_dto.count
    assert task.task_type == TaskType.placing
    assert task.acceptance_id == created_acceptance_in_db.id


async def test_create_acceptance_existing_sku_success(
    client: AsyncClient,
    acceptance_repository: AcceptanceRepository,
    task_repository: TaskRepository,
    sku_in_db: SkuDTO,
    create_acceptance_item_input_dto: CreateAcceptanceItemInputDTO,
):
    items_to_accept = [
        create_acceptance_item_input_dto.model_copy(
            update={"sku_id": sku_in_db.id}
        )
    ]

    created_acceptance_from_response = await send_request_return_output_dto(
        client=client,
        items_to_accept=items_to_accept
    )

    created_acceptance_in_db = await acceptance_repository.get_by_id(
        created_acceptance_from_response.id
    )

    created_tasks_in_db = await task_repository.get_by_acceptance_id(
        created_acceptance_in_db.id
    )

    task = created_tasks_in_db[0]

    assert len(created_tasks_in_db) == len(items_to_accept)

    assert task.sku_id == sku_in_db.id
    assert task.stock == create_acceptance_item_input_dto.stock
    assert task.count == create_acceptance_item_input_dto.count
    assert task.task_type == TaskType.placing
    assert task.acceptance_id == created_acceptance_in_db.id


async def test_create_acceptance_non_existing_and_existing_sku_success(
    client: AsyncClient,
    acceptance_repository: AcceptanceRepository,
    task_repository: TaskRepository,
    sku_in_db: SkuDTO,
    create_acceptance_item_input_dto: CreateAcceptanceItemInputDTO,
):
    items_to_accept = [
        create_acceptance_item_input_dto,
        create_acceptance_item_input_dto.model_copy(
            update={"sku_id": sku_in_db.id}
        )
    ]

    created_acceptance_from_response = await send_request_return_output_dto(
        client=client,
        items_to_accept=items_to_accept
    )

    created_acceptance_in_db = await acceptance_repository.get_by_id(
        created_acceptance_from_response.id
    )

    created_tasks_in_db = await task_repository.get_by_acceptance_id(
        created_acceptance_in_db.id
    )

    assert len(created_tasks_in_db) == len(items_to_accept)

    assert {task.sku_id for task in created_tasks_in_db} == {
        item.sku_id for item in items_to_accept
    }

    for task in created_tasks_in_db:
        assert task.stock == create_acceptance_item_input_dto.stock
        assert task.count == create_acceptance_item_input_dto.count
        assert task.task_type == TaskType.placing
        assert task.acceptance_id == created_acceptance_in_db.id
