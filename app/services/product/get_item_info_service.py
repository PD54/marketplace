import logging
from uuid import UUID

from app.database.repositories.product import ProductRepository
from app.database.repositories.sku import SkuRepository
from app.services.product.dto.get_item_info import GetItemInfoOutputDTO
from app.services.product.exceptions import ItemNotFoundError
from app.services.sku.exceptions import SkuNotFoundError

logger = logging.getLogger(__name__)


class GetItemInfoService:
    def __init__(
        self,
        product_repo: ProductRepository,
        sku_repo: SkuRepository
    ):
        self.product_repo = product_repo
        self.sku_repo = sku_repo
    
    async def get_item_info(self, product_id: UUID) -> GetItemInfoOutputDTO:
        logger.info(f"Поиск товара с id {product_id}")
        product = await self.product_repo.get_by_id(entity_id=product_id)
        if not product:
            logger.error(f"Не найден товар с id {product_id}")
            raise ItemNotFoundError()

        logger.info(f"Поиск SKU с id {product.sku_id}")
        sku = await self.sku_repo.get_by_id(entity_id=product.sku_id)
        if not sku:
            logger.error(f"Не найдена SKU с id {product.sku_id}")
            raise SkuNotFoundError()

        logger.info(f"Успешно найдены товар и его SKU")
        return GetItemInfoOutputDTO.model_validate(product)
