import logging

from app.database.dto.good import UpdateGoodDTO
from app.database.dto.posting_good import PostingGoodDTO
from app.database.dto.task import TaskDTO, TaskType
from app.database.repositories.good import GoodRepository
from app.database.repositories.posting_good import PostingGoodRepository
from app.database.repositories.task import TaskRepository

logger = logging.getLogger(__name__)


class PickNewGoodForPostingService:
    def __init__(
        self,
        good_repo: GoodRepository,
        task_repo: TaskRepository,
        posting_good_repo: PostingGoodRepository,
    ):
        self.good_repo = good_repo
        self.task_repo = task_repo
        self.posting_good_repo = posting_good_repo

    async def pick_new_good(
        self,
        posting_good: PostingGoodDTO,
    ) -> PostingGoodDTO | None:
        logger.info("Поиск товара для замены")
        replacement_good = (
            await self.good_repo.pick_available_by_sku_and_stock(
                posting_good.good_sku_id,
                posting_good.good_stock,
            )
        )

        if not replacement_good:
            logger.info("Не найден товар для замены")
            return None
        logger.info(f"Найден товар для замены с id {replacement_good.id}")

        replacement_posting_good = await self.posting_good_repo.create(
            PostingGoodDTO(
                posting_id=posting_good.posting_id,
                good_id=replacement_good.id,
                good_sku_id=replacement_good.sku_id,
                good_cost=posting_good.good_cost,
                good_stock=replacement_good.stock,
            ),
        )
        logger.info(
            f"Товар для замены {replacement_good.id} "
            f"добавлен в заказ {replacement_posting_good.posting_id}"
        )

        replacement_task = await self.task_repo.create(
            TaskDTO(
                task_type=TaskType.picking,
                posting_id=posting_good.posting_id,
                good_id=replacement_good.id,
                sku_id=replacement_good.sku_id,
                stock=replacement_good.stock,
                count=1,
            ),
        )
        logger.info(
            f"Создана задача на подбор с id {replacement_task.id}"
            f", заменяющая отменённую задачу на подбор"
        )

        await self.good_repo.update(
            entity_id=replacement_good.id,
            update_dto=UpdateGoodDTO(reserved_state=True),
        )
        logger.info(
            f"Товар для замены с id {replacement_good.id} зарезервирован"
        )

        return replacement_posting_good
