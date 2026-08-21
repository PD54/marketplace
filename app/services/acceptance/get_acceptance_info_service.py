import logging
from uuid import UUID

from app.database.dto.task import TaskDTO, TaskStatus
from app.database.repositories.acceptance import AcceptanceRepository
from app.database.repositories.task import TaskRepository
from app.services.acceptance.dto.get_acceptance_info import (
    GetAcceptanceInfoAcceptedItemOutputDTO,
    GetAcceptanceInfoOutputDTO,
    GetAcceptanceInfoTaskOutputDTO,
)
from app.services.acceptance.exceptions import AcceptanceNotFoundError

logger = logging.getLogger(__name__)


class GetAcceptanceInfoService:
    def __init__(
        self,
        acceptance_repo: AcceptanceRepository,
        task_repo: TaskRepository,
    ):
        self.acceptance_repo = acceptance_repo
        self.task_repo = task_repo

    async def get_acceptance_info(
        self,
        acceptance_id: UUID,
    ) -> GetAcceptanceInfoOutputDTO:
        logger.info(f"Обработка приёмки с id {acceptance_id}")

        acceptance = await self.acceptance_repo.get_by_id(acceptance_id)
        if not acceptance:
            logger.error(f"Не найдена приемка с id {acceptance_id}")
            raise AcceptanceNotFoundError()
        logger.info(f"Найдена приёмка с id {acceptance_id}")

        tasks = await self.task_repo.get_by_acceptance_id(acceptance_id)

        return GetAcceptanceInfoOutputDTO(
            id=acceptance_id,
            created_at=acceptance.created_at,
            accepted=self.get_accepted_items(tasks),
            task_ids=self.get_task_ids(tasks),
        )

    @staticmethod
    def get_accepted_items(
        tasks: list[TaskDTO],
    ) -> list[GetAcceptanceInfoAcceptedItemOutputDTO]:
        return [
            GetAcceptanceInfoAcceptedItemOutputDTO.model_validate(task)
            for task in tasks
            if task.status == TaskStatus.completed
        ]

    @staticmethod
    def get_task_ids(
        tasks: list[TaskDTO],
    ) -> list[GetAcceptanceInfoTaskOutputDTO]:
        return [
            GetAcceptanceInfoTaskOutputDTO.model_validate(task)
            for task in tasks
        ]
