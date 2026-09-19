import logging

from app.database.dto.sku import UpdateSkuDTO
from app.database.repositories.sku import SkuRepository
from app.services.sku.dto.set_sku_price import SetSkuPriceInputDTO
from app.services.sku.exceptions import SkuNotFoundError

logger = logging.getLogger(__name__)


class SetSkuPriceService:
    def __init__(self, sku_repo: SkuRepository):
        self.sku_repo = sku_repo

    async def set_sku_price(self, input_dto: SetSkuPriceInputDTO) -> None:
        logger.info(
            f"Установка цены SKU с id {input_dto.sku_id}"
            f" на {input_dto.base_price}"
        )

        sku = await self.sku_repo.get_by_id(input_dto.sku_id)
        if not sku:
            logger.error(f"SKU с id {input_dto.sku_id} не найдена")
            raise SkuNotFoundError()

        await self.sku_repo.update(
            entity_id=input_dto.sku_id,
            update_dto=UpdateSkuDTO(base_price=input_dto.base_price),
        )
        logger.info("Цена SKU установлена")
