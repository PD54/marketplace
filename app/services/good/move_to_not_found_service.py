import logging

from app.database.dto.good import GoodDTO, GoodStock, UpdateGoodDTO
from app.database.dto.task import TaskDTO, TaskStatus, TaskType, UpdateTaskDTO
from app.database.repositories.good import GoodRepository
from app.database.repositories.task import TaskRepository
from app.services.good.dto.move_to_not_found import MoveToNotFoundInputDTO
from app.services.good.exceptions import GoodNotFoundError
from app.services.task.replace_task_and_good import ReplaceTaskAndGoodService

logger = logging.getLogger(__name__)


class MoveToNotFoundService:
    def __init__(
        self,
        good_repo: GoodRepository,
        task_repo: TaskRepository,
        replace_task_and_good_service: ReplaceTaskAndGoodService,
    ):
        self.good_repo = good_repo
        self.task_repo = task_repo
        self.replace_task_and_good_service = replace_task_and_good_service

    async def move_to_not_found(
        self,
        input_dto: MoveToNotFoundInputDTO,
    ) -> None:
        logger.info(f"Перемещение товара {input_dto.id} на сток not_found")
        updated_good = await self.good_repo.update(
            entity_id=input_dto.id,
            update_dto=UpdateGoodDTO(
                stock=GoodStock.not_found,
                reserved_state=False,
            ),
        )
        if not updated_good:
            logger.error(f"Товар {input_dto.id} не найден")
            raise GoodNotFoundError()
        logger.info(
            f"Товар {updated_good.id} перемещён на сток {updated_good.stock};"
            f" reserved_state установлен в {updated_good.reserved_state}"
        )

        just_cancelled_tasks = await self.cancel_related_tasks(updated_good)

        for task in just_cancelled_tasks:
            if task.task_type == TaskType.placing:
                continue

            await self.replace_task_and_good_service.replace_task_and_good(
                task,
            )

    async def cancel_related_tasks(
        self,
        updated_good: GoodDTO,
    ) -> list[TaskDTO]:
        tasks = await self.task_repo.get_by_good_id(updated_good.id)
        logger.info(f"Найдено {len(tasks)} задач")

        just_cancelled_tasks = []
        for task in tasks:
            if (
                task.status == TaskStatus.in_work
                or task.status == TaskStatus.completed
            ):
                just_cancelled_task = await self.task_repo.update(
                    entity_id=task.id,
                    update_dto=UpdateTaskDTO(
                        status=TaskStatus.cancelled,
                    ),
                )

                if just_cancelled_task:
                    just_cancelled_tasks.append(just_cancelled_task)

        logger.info(f"Отменено {len(just_cancelled_tasks)} задач")

        return just_cancelled_tasks
