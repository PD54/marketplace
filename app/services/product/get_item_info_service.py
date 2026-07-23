from uuid import UUID

from app.database.repositories.product import ProductRepository
from app.database.repositories.sku import SkuRepository
from app.services.product.dto.get_item_info import GetItemInfoResponse
from app.services.product.exceptions import ItemNotFoundError
from app.services.sku.exceptions import SkuNotFoundError


class GetItemInfoService:
    def __init__(
        self,
        product_repo: ProductRepository,
        sku_repo: SkuRepository
    ):
        self.product_repo = product_repo
        self.sku_repo = sku_repo
    
    async def get_item_info(self, product_id: UUID) -> GetItemInfoResponse:
        product = await self.product_repo.get_by_id(entity_id=product_id)
        if not product:
            raise ItemNotFoundError()
        
        sku = await self.sku_repo.get_by_id(entity_id=product.sku_id)
        if not sku:
            raise SkuNotFoundError()
        
        return GetItemInfoResponse.model_validate(product)
