import logging
from uuid import UUID

from app.database.repositories.good import GoodRepository
from app.services.good.dto.get_item_info_by_sku_id import (
    GetItemInfoBySkuIdItemOutputDTO,
    GetItemInfoBySkuIdOutputDTO,
)

logger = logging.getLogger(__name__)


class GetItemInfoBySkuIdService:
    def __init__(self, good_repo: GoodRepository):
        self.good_repo = good_repo

    async def get_item_info_by_sku_id(
        self,
        sku_id: UUID,
    ) -> GetItemInfoBySkuIdOutputDTO:
        logger.info(f"Получение товаров по SKU с id {sku_id}")

        goods = await self.good_repo.get_all_by_sku_id(sku_id)
        logger.info(f"Найдено {len(goods)} товаров")

        items = [
            GetItemInfoBySkuIdItemOutputDTO(
                item_id=good.id,
                stock=good.stock,
                reserved_state=good.reserved_state,
            )
            for good in goods
        ]

        return GetItemInfoBySkuIdOutputDTO(items=items)
