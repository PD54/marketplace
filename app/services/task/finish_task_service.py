import logging

from app.database.dto.good import (
    GoodDTO,
    GoodReservedState,
    GoodStock,
    UpdateGoodDTO,
)
from app.database.dto.posting import PostingStatus, UpdatePostingDTO
from app.database.dto.posting_good import (
    PostingGoodCancelReason,
    UpdatePostingGoodDTO,
)
from app.database.dto.task import (
    TaskDTO,
    TaskStatus,
    TaskStatusWithoutInWork,
    TaskType,
    UpdateTaskDTO,
)
from app.database.repositories.acceptance import AcceptanceRepository
from app.database.repositories.good import GoodRepository
from app.database.repositories.posting import PostingRepository
from app.database.repositories.posting_good import PostingGoodRepository
from app.database.repositories.task import TaskRepository
from app.services.task.dto.finish_task import FinishTaskInputDTO
from app.services.task.exceptions import TaskNotFoundError

logger = logging.getLogger(__name__)


class FinishTaskService:
    def __init__(
        self,
        task_repo: TaskRepository,
        good_repo: GoodRepository,
        acceptance_repo: AcceptanceRepository,
        posting_repo: PostingRepository,
        posting_good_repo: PostingGoodRepository,
    ):
        self.task_repo = task_repo
        self.good_repo = good_repo
        self.acceptance_repo = acceptance_repo
        self.posting_repo = posting_repo
        self.posting_good_repo = posting_good_repo

    async def finish_task(self, input_dto: FinishTaskInputDTO) -> None:
        logger.info(
            f"Завершение задачи с id {input_dto.id},"
            f" статус - {input_dto.status}"
        )

        task = await self.task_repo.get_by_id(input_dto.id)
        if not task:
            logger.error(f"Задача с id {input_dto.id} не найдена в БД")
            raise TaskNotFoundError()

        if task.status != TaskStatus.in_work:
            logger.info(f"Задача с id {input_dto.id} уже завершена")
            return

        await self.task_repo.update(
            entity_id=input_dto.id,
            update_dto=UpdateTaskDTO(
                status=input_dto.status,
            ),
        )
        logger.info(
            f"Задача с id {input_dto.id} завершена,"
            f" новый статус - {input_dto.status}"
        )

        await self.handle_finished_task(
            task=task,
            final_status=input_dto.status,
        )

    async def handle_finished_task(
        self,
        task: TaskDTO,
        final_status: TaskStatusWithoutInWork,
    ) -> None:
        if task.task_type == TaskType.picking:
            await self.handle_picking_task(
                task=task,
                final_status=final_status,
            )
            return

        if task.task_type == TaskType.placing:
            await self.handle_placing_task(
                task=task,
                final_status=final_status,
            )
            return

    async def handle_picking_task(
        self,
        task: TaskDTO,
        final_status: TaskStatusWithoutInWork,
    ) -> None:
        if task.posting_id:
            if final_status == TaskStatus.completed:
                await self.handle_picking_completed_posting_task(
                    task=task,
                )
                return

            if final_status == TaskStatus.cancelled:
                await self.handle_picking_cancelled_posting_task(
                    task=task,
                )
                return

    async def handle_placing_task(
        self,
        task: TaskDTO,
        final_status: TaskStatusWithoutInWork,
    ) -> None:
        if task.posting_id:
            if final_status == TaskStatus.completed:
                await self.handle_placing_completed_posting_task(
                    task=task,
                )
                return

            if final_status == TaskStatus.cancelled:
                await self.handle_placing_cancelled_posting_task(
                    task=task,
                )
                return

        if task.acceptance_id:
            if final_status == TaskStatus.completed:
                await self.handle_placing_completed_acceptance_task(
                    task=task,
                )
                return

            if final_status == TaskStatus.cancelled:
                logger.info(
                    "Задача приёмки отменена, дальнейших действий не требуется"
                )
                return

    async def handle_picking_completed_posting_task(
        self,
        task: TaskDTO,
    ) -> None:
        logger.info(
            f"Завершена picking задача заказа с id {task.posting_id}."
            f" Проверка, можно ли отправлять заказ."
        )
        tasks = await self.task_repo.get_by_posting_id(task.posting_id)  # type: ignore

        if TaskStatus.in_work in [task.status for task in tasks]:
            logger.info(
                f"В заказе с id {task.posting_id} остались in-work задачи"
            )
            return

        await self.posting_repo.update(
            entity_id=task.posting_id,  # type: ignore
            update_dto=UpdatePostingDTO(
                status=PostingStatus.sent,
            ),
        )
        logger.info(
            f"Статус заказа с id {task.posting_id}"
            f" обновлён на {PostingStatus.sent}"
        )

        posting_goods = await self.posting_good_repo.get_by_posting_id(
            task.posting_id,  # type: ignore
        )
        good_ids = [
            posting_good.good_id
            for posting_good in posting_goods
            if not posting_good.cancel_reason
        ]
        await self.good_repo.bulk_update(
            entity_ids_list=good_ids,
            update_dto=UpdateGoodDTO(
                reserved_state=GoodReservedState.sold,
            ),
        )
        logger.info(
            f"У {len(good_ids)} товаров"
            f" статус резервирования установлен в {GoodReservedState.sold}"
        )

    async def handle_picking_cancelled_posting_task(
        self,
        task: TaskDTO,
    ) -> None:
        logger.info(
            f"Отменена picking задача заказа с id {task.posting_id}."
            f" Отмена резервирования товаров,"
            f" проверка возможности отмены заказа."
        )

        posting_goods = await self.posting_good_repo.get_by_posting_id(
            task.posting_id,  # type: ignore
        )
        posting_goods_with_task_good_ids = []
        goods_ids = []
        for posting_good in posting_goods:
            if (
                posting_good.cancel_reason
                or posting_good.good_id != task.good_id
            ):
                continue

            posting_goods_with_task_good_ids.append(posting_good.id)
            goods_ids.append(posting_good.good_id)

        await self.posting_good_repo.bulk_update(
            entity_ids_list=posting_goods_with_task_good_ids,
            update_dto=UpdatePostingGoodDTO(
                cancel_reason=PostingGoodCancelReason.task_cancelled,
            ),
        )
        logger.info(
            f"Отменено {len(posting_goods_with_task_good_ids)}"
            f" упоминаний товара в заказе"
        )
        await self.good_repo.bulk_update(
            entity_ids_list=goods_ids,
            update_dto=UpdateGoodDTO(
                reserved_state=GoodReservedState.unreserved,
            ),
        )
        logger.info(f"Резервирование снято у {len(goods_ids)} товаров")

        tasks = await self.task_repo.get_by_posting_id(task.posting_id)  # type: ignore

        has_not_cancelled_tasks = False

        for task in tasks:
            if task.status != TaskStatus.cancelled:
                has_not_cancelled_tasks = True
                break

        if has_not_cancelled_tasks:
            logger.info(
                f"Заказ с id {task.posting_id} имеет неотменённые задачи"
            )
            return

        await self.posting_repo.update(
            entity_id=task.posting_id,  # type: ignore
            update_dto=UpdatePostingDTO(
                status=PostingStatus.cancelled,
            ),
        )
        logger.info(
            f"Заказ с id {task.posting_id}"
            f" больше не имеет неотменённых задач, и был отменён"
        )

    async def handle_placing_completed_posting_task(
        self,
        task: TaskDTO,
    ) -> None:
        logger.info(
            f"Завершена placing задача заказа с id {task.posting_id}."
            f" Снятие резерва с товара."
        )

        await self.good_repo.update(
            entity_id=task.good_id,  # type: ignore
            update_dto=UpdateGoodDTO(
                reserved_state=GoodReservedState.unreserved
            ),
        )
        logger.info(
            f"Товар с id {task.good_id} помечен"
            f" как {GoodReservedState.unreserved}"
        )

    async def handle_placing_cancelled_posting_task(
        self,
        task: TaskDTO,
    ) -> None:
        logger.info(
            f"Отменена placing задача заказа с id {task.posting_id}."
            f" Перемещение товара на {GoodStock.not_found} сток,"
            f" снятие резервации с товара."
        )

        await self.good_repo.update(
            entity_id=task.good_id,  # type: ignore
            update_dto=UpdateGoodDTO(
                reserved_state=GoodReservedState.unreserved,
                stock=GoodStock.not_found,
            ),
        )
        logger.info(
            f"Товар с id {task.good_id}"
            f" получил статус резервации {GoodReservedState.unreserved},"
            f" перемещён на сток {GoodStock.not_found}"
        )

    async def handle_placing_completed_acceptance_task(
        self,
        task: TaskDTO,
    ) -> None:
        logger.info(
            f"Завершена picking задача приёмки c id {task.acceptance_id}."
            f" Добавление товаров на сток."
        )

        await self.good_repo.bulk_create(
            [
                GoodDTO(
                    sku_id=task.sku_id,
                    stock=task.stock,
                )
                for _ in range(task.count)
            ]
        )
        logger.info(f"{task.count} товаров добавлено на сток {task.stock}")
