import logging
from uuid import UUID

from app.database.dto.discount import DiscountDTO, DiscountStatus
from app.database.repositories.discount import DiscountRepository
from app.database.repositories.good import GoodRepository
from app.database.repositories.sku import SkuRepository
from app.database.repositories.sku_and_discount import SkuAndDiscountRepository
from app.services.sku.dto.get_sku_info import GetSkuInfoOutputDTO
from app.services.sku.exceptions import SkuNotFoundError
from app.utils.sku_actual_price import calculate_sku_actual_price

logger = logging.getLogger(__name__)


class GetSkuInfoService:
    def __init__(
        self,
        sku_repo: SkuRepository,
        discount_repo: DiscountRepository,
        sku_and_discount_repo: SkuAndDiscountRepository,
        good_repo: GoodRepository,
    ):
        self.sku_repo = sku_repo
        self.discount_repo = discount_repo
        self.sku_and_discount_repo = sku_and_discount_repo
        self.good_repo = good_repo

    async def get_sku_info(self, sku_id: UUID) -> GetSkuInfoOutputDTO:
        logger.info(f"Получение информации о SKU с id {sku_id}")

        sku = await self.sku_repo.get_by_id(sku_id)
        if not sku:
            logger.error(f"SKU с id {sku_id} не найдена")
            raise SkuNotFoundError()

        goods_in_sku = await self.good_repo.get_all_by_sku_id(sku_id)
        count = len(goods_in_sku)
        logger.info(f"Найдено товаров на всех стоках: {count}")

        active_discounts = await self.get_active_discounts(sku_id)
        actual_price = calculate_sku_actual_price(
            sku=sku,
            active_discounts=active_discounts,
        )

        return GetSkuInfoOutputDTO(
            id=sku_id,
            created_at=sku.created_at,
            actual_price=actual_price,
            base_price=sku.base_price,
            count=count,
            is_hidden=sku.is_hidden,
        )

    async def get_active_discounts(self, sku_id: UUID) -> list[DiscountDTO]:
        logger.info(f"Поиск активных скидок для SKU с id {sku_id}")

        sku_discounts = await self.sku_and_discount_repo.get_by_sku_id(sku_id)
        discounts_ids = [
            sku_discount.discount_id for sku_discount in sku_discounts
        ]
        discounts = await self.discount_repo.get_all_by_ids(discounts_ids)
        logger.info(f"Найдено {len(discounts)} всего скидок для SKU")

        active_discounts = [
            discount
            for discount in discounts
            if discount.status == DiscountStatus.active
        ]
        logger.info(f"Найдено {len(active_discounts)} активных скидок для SKU")

        return active_discounts
