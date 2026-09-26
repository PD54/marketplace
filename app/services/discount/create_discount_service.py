import logging

from app.database.dto.discount import DiscountDTO
from app.database.dto.sku_and_discount import SkuAndDiscountDTO
from app.database.repositories.discount import DiscountRepository
from app.database.repositories.sku import SkuRepository
from app.database.repositories.sku_and_discount import SkuAndDiscountRepository
from app.services.discount.dto.create_discount import (
    CreateDiscountInputDTO,
    CreateDiscountOutputDTO,
)
from app.services.sku.exceptions import SkuNotFoundError

logger = logging.getLogger(__name__)


class CreateDiscountService:
    def __init__(
        self,
        sku_repo: SkuRepository,
        discount_repo: DiscountRepository,
        sku_and_discount_repo: SkuAndDiscountRepository,
    ):
        self.sku_repo = sku_repo
        self.discount_repo = discount_repo
        self.sku_and_discount_repo = sku_and_discount_repo

    async def create_discount(
        self,
        input_dto: CreateDiscountInputDTO,
    ) -> CreateDiscountOutputDTO:
        logger.info(f"Создание скидки для {len(input_dto.sku_ids)} SKU")

        skus = await self.sku_repo.get_all_by_ids(input_dto.sku_ids)
        skus_in_db_ids = [sku.id for sku in skus]
        if sorted(input_dto.sku_ids) != sorted(skus_in_db_ids):
            non_existing_sku_ids = list(
                set(input_dto.sku_ids) - set(skus_in_db_ids)
            )
            logger.error(
                f"Некоторые из SKU не найдены в БД: {non_existing_sku_ids=}"
            )
            raise SkuNotFoundError()

        discount = await self.discount_repo.create(
            DiscountDTO(
                percentage=input_dto.percentage,
            )
        )
        logger.info(f"Создана скидка с id {discount.id}")

        await self.sku_and_discount_repo.bulk_create(
            [
                SkuAndDiscountDTO(
                    discount_id=discount.id,
                    sku_id=sku_id,
                )
                for sku_id in input_dto.sku_ids
            ]
        )
        logger.info("Созданы связи скидки и SKU")

        return CreateDiscountOutputDTO(id=discount.id)
