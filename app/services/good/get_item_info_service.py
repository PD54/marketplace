import logging
from uuid import UUID

from app.database.repositories.good import GoodRepository
from app.database.repositories.sku import SkuRepository
from app.services.good.dto.get_item_info import GetItemInfoOutputDTO
from app.services.good.exceptions import ItemNotFoundError
from app.services.sku.exceptions import SkuNotFoundError

logger = logging.getLogger(__name__)


class GetItemInfoService:
    def __init__(
        self,
        good_repo: GoodRepository,
        sku_repo: SkuRepository,
    ):
        self.good_repo = good_repo
        self.sku_repo = sku_repo

    async def get_item_info(self, good_id: UUID) -> GetItemInfoOutputDTO:
        logger.info(f"Поиск товара с id {good_id}")
        good = await self.good_repo.get_by_id(entity_id=good_id)
        if not good:
            logger.error(f"Не найден товар с id {good_id}")
            raise ItemNotFoundError()

        logger.info(f"Поиск SKU с id {good.sku_id}")
        sku = await self.sku_repo.get_by_id(entity_id=good.sku_id)
        if not sku:
            logger.error(f"Не найдена SKU с id {good.sku_id}")
            raise SkuNotFoundError()

        logger.info("Успешно найдены товар и его SKU")
        return GetItemInfoOutputDTO.model_validate(good)
