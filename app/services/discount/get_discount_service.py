import logging
from uuid import UUID

from app.database.repositories.discount import DiscountRepository
from app.database.repositories.sku_and_discount import SkuAndDiscountRepository
from app.services.discount.dto.get_discount import GetDiscountOutputDTO
from app.services.discount.exceptions import DiscountNotFoundError

logger = logging.getLogger(__name__)


class GetDiscountService:
    def __init__(
        self,
        discount_repo: DiscountRepository,
        sku_and_discount_repo: SkuAndDiscountRepository,
    ):
        self.discount_repo = discount_repo
        self.sku_and_discount_repo = sku_and_discount_repo

    async def get_discount(
        self,
        discount_id: UUID,
    ) -> GetDiscountOutputDTO:
        logger.info(f"Получение информации о скидке с id {discount_id}")

        discount = await self.discount_repo.get_by_id(discount_id)
        if not discount:
            logger.error(f"Скидка с id {discount_id} не найдена")
            raise DiscountNotFoundError()

        sku_and_discounts_list = (
            await self.sku_and_discount_repo.get_by_discount_id(discount_id)
        )
        logger.info(f"Найдено {len(sku_and_discounts_list)} связанных SKU")

        return GetDiscountOutputDTO(
            id=discount_id,
            status=discount.status,
            created_at=discount.created_at,
            percentage=discount.percentage,
            sku_ids=[
                sku_and_discount.sku_id
                for sku_and_discount in sku_and_discounts_list
            ],
        )
