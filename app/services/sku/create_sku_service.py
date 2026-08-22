import logging

from sqlalchemy.exc import IntegrityError

from app.database.dto.sku import SkuDTO
from app.database.repositories.sku import SkuRepository
from app.services.sku.dto.create_sku import (
    CreateSkuInputDTO,
    CreateSkuOutputDTO,
)
from app.services.sku.exceptions import SkuAlreadyExistsError

logger = logging.getLogger(__name__)


class CreateSkuService:
    def __init__(self, sku_repo: SkuRepository):
        self.sku_repo = sku_repo

    async def create_sku(
        self,
        input_dto: CreateSkuInputDTO,
    ) -> CreateSkuOutputDTO:
        try:
            logger.info(f"Попытка создать SKU с id {input_dto.id}")
            sku = await self.sku_repo.create(SkuDTO.model_validate(input_dto))
        except IntegrityError:
            logger.error(f"SKU с id {input_dto.id} уже cуществует")
            raise SkuAlreadyExistsError()

        logger.info(f"Успешно создана SKU с id {sku.id}")
        return CreateSkuOutputDTO.model_validate(sku)
