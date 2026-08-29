from uuid import uuid7

from httpx import AsyncClient

from app.database.dto.acceptance import AcceptanceDTO
from app.database.dto.task import TaskDTO
from app.services.acceptance.dto.get_acceptance_info import (
    GetAcceptanceInfoAcceptedItemOutputDTO,
    GetAcceptanceInfoOutputDTO,
)


async def test_get_acceptance_info_success(
    client: AsyncClient,
    acceptance_in_db: AcceptanceDTO,
    tasks_from_acceptance_in_db: list[TaskDTO],
    task_from_acceptance_dto: TaskDTO,
):
    response = await client.get(f"getAcceptanceInfo?id={acceptance_in_db.id}")

    actual_output_dto = GetAcceptanceInfoOutputDTO.model_validate(
        response.json(),
    )

    expected_accepted = [
        GetAcceptanceInfoAcceptedItemOutputDTO.model_validate(
            task_from_acceptance_dto,
        )
    ]

    assert actual_output_dto.id == acceptance_in_db.id
    assert actual_output_dto.created_at == acceptance_in_db.created_at
    assert actual_output_dto.accepted == expected_accepted

    assert len(actual_output_dto.task_ids) == len(tasks_from_acceptance_in_db)
    assert {task.id for task in actual_output_dto.task_ids} == {
        task.id for task in tasks_from_acceptance_in_db
    }


async def test_get_acceptance_info_not_found(
    client: AsyncClient,
):
    random_id = uuid7()
    response = await client.get(url=f"getAcceptanceInfo?id={random_id}")

    assert response.status_code == 404
    assert response.json()["detail"] == "Acceptance not found"
