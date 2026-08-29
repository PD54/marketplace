import logging

from app.database.dto.good import UpdateGoodDTO
from app.database.dto.task import TaskDTO
from app.database.repositories.good import GoodRepository
from app.database.repositories.task import TaskRepository

logger = logging.getLogger(__name__)


class ReplaceTaskAndGoodService:
    def __init__(self, good_repo: GoodRepository, task_repo: TaskRepository):
        self.good_repo = good_repo
        self.task_repo = task_repo

    async def replace_task_and_good(self, task: TaskDTO) -> TaskDTO | None:
        logger.info("Поиск товара для замены")
        replacement_good = await self.good_repo.grab_avail_by_sku_and_stock(
            task.sku_id,
            task.stock,
        )

        if not replacement_good:
            logger.info("Не найден товар для замены")
            return None
        logger.info(f"Найден товар для замены с id {replacement_good.id}")

        replacement_task = await self.task_repo.create(
            TaskDTO(
                task_type=task.task_type,
                posting_id=task.posting_id,
                good_id=replacement_good.id,
                sku_id=replacement_good.sku_id,
                stock=replacement_good.stock,
                count=1,
            ),
        )
        logger.info(
            f"Создана задача на подбор с id {replacement_task.id}"
            f", заменяющая отменённую задачу на подбор с id {task.id}"
        )

        await self.good_repo.update(
            replacement_good.id,
            UpdateGoodDTO(reserved_state=True),
        )
        logger.info(
            f"Товар для замены с id {replacement_good.id} зарезервирован"
        )

        return replacement_task
