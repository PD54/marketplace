import logging

from app.database.dto.sku import UpdateSkuDTO
from app.database.repositories.sku import SkuRepository
from app.services.sku.dto.toggle_is_hidden import ToggleIsHiddenInputDTO
from app.services.sku.exceptions import SkuNotFoundError

logger = logging.getLogger(__name__)


class ToggleIsHiddenService:
    def __init__(self, sku_repo: SkuRepository):
        self.sku_repo = sku_repo

    async def toggle_is_hidden(
        self,
        input_dto: ToggleIsHiddenInputDTO,
    ) -> None:
        logger.info(
            f"SKU {input_dto.sku_id}: смена is_hidden на {input_dto.is_hidden}"
        )
        result = await self.sku_repo.update(
            entity_id=input_dto.sku_id,
            update_dto=UpdateSkuDTO(is_hidden=input_dto.is_hidden),
        )

        if not result:
            logger.error(f"SKU с id {input_dto.sku_id} не найдена")
            raise SkuNotFoundError()

        logger.info(
            f"SKU {input_dto.sku_id}: "
            f"значение is_hidden изменено на {input_dto.is_hidden}"
        )
