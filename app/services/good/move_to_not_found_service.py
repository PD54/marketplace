import logging

from app.database.dto.good import GoodDTO, GoodStock, UpdateGoodDTO
from app.database.dto.posting_good import (
    PostingGoodCancelReason,
    PostingGoodDTO,
    UpdatePostingGoodDTO,
)
from app.database.dto.task import TaskStatus, UpdateTaskDTO
from app.database.repositories.good import GoodRepository
from app.database.repositories.posting_good import PostingGoodRepository
from app.database.repositories.task import TaskRepository
from app.services.good.dto.move_to_not_found import MoveToNotFoundInputDTO
from app.services.good.exceptions import (
    GoodAlreadyOnNotFoundStockError,
    GoodNotFoundError,
)
from app.services.posting_good.pick_new_good_for_posting_service import (
    PickNewGoodForPostingService,
)

logger = logging.getLogger(__name__)


class MoveToNotFoundService:
    def __init__(
        self,
        good_repo: GoodRepository,
        task_repo: TaskRepository,
        posting_good_repo: PostingGoodRepository,
        pick_new_good_for_posting_service: PickNewGoodForPostingService,
    ):
        self.good_repo = good_repo
        self.task_repo = task_repo
        self.posting_good_repo = posting_good_repo
        self.pick_new_good_for_posting_service = (
            pick_new_good_for_posting_service
        )

    async def move_to_not_found(
        self,
        input_dto: MoveToNotFoundInputDTO,
    ) -> None:
        logger.info(f"Перемещение товара {input_dto.id} на сток not_found")
        good = await self.good_repo.get_by_id(input_dto.id)
        if not good:
            logger.error(f"Товар с id {input_dto.id} не найден")
            raise GoodNotFoundError()

        if good.stock == GoodStock.not_found:
            logger.error(f"Товар с id {input_dto.id} уже на стоке not_found")
            raise GoodAlreadyOnNotFoundStockError()

        await self.good_repo.update(
            entity_id=input_dto.id,
            update_dto=UpdateGoodDTO(
                stock=GoodStock.not_found,
                reserved_state=False,
            ),
        )
        logger.info(
            f"Товар {good.id} перемещён на сток not_found;"
            f" reserved_state установлен в False"
        )

        cancelled_posting_goods = await self.cancel_posting_goods(good)

        await self.cancel_related_tasks(good)

        for cancelled_posting_good in cancelled_posting_goods:
            await self.pick_new_good_for_posting_service.pick_new_good(
                cancelled_posting_good,
            )

    async def cancel_posting_goods(
        self,
        updated_good: GoodDTO,
    ) -> list[PostingGoodDTO]:
        posting_goods = await self.posting_good_repo.get_by_good_id(
            updated_good.id,
        )
        logger.info(
            f"Найдено {len(posting_goods)} записей с товаром в заказах"
        )

        posting_goods_to_cancel = [
            posting_good
            for posting_good in posting_goods
            if not posting_good.cancel_reason
        ]

        for posting_good in posting_goods_to_cancel:
            await self.posting_good_repo.update(
                entity_id=posting_good.id,
                update_dto=UpdatePostingGoodDTO(
                    cancel_reason=PostingGoodCancelReason.good_not_found,
                ),
            )
            logger.info(
                f"Отменена запись с id {posting_good.id} с товаром в заказе"
            )

        logger.info(
            f"Итого отменено {len(posting_goods_to_cancel)} "
            f"записей с товаром в заказах"
        )

        return posting_goods_to_cancel

    async def cancel_related_tasks(
        self,
        updated_good: GoodDTO,
    ) -> None:
        tasks = await self.task_repo.get_by_good_id(updated_good.id)
        logger.info(f"Найдено {len(tasks)} задач")

        cancelled_tasks_count = 0
        for task in tasks:
            if task.status != TaskStatus.in_work:
                continue

            await self.task_repo.update(
                entity_id=task.id,
                update_dto=UpdateTaskDTO(
                    status=TaskStatus.cancelled,
                ),
            )
            cancelled_tasks_count += 1
            logger.info(
                f"Отменена связанная с товаром активная задача с id {task.id}"
            )

        logger.info(
            f"Отменено {cancelled_tasks_count} связанных активных задач"
        )
