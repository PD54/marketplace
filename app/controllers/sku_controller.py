from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.pydantic_schemas.responses.get_item_info import GetItemInfoResponse
from app.dependencies.session_generator import get_db
from app.exceptions.http_exceptions import NotFoundError
from app.models.product import ProductORM
from app.models.sku import SkuORM

router = APIRouter(tags=["SkuController"])


@router.get("/getItemInfo")
async def get_item_info(
    id: UUID,
    database: AsyncSession = Depends(get_db)
) -> GetItemInfoResponse:
    product = await database.get(ProductORM, id)
    if not product:
        raise NotFoundError()
    
    sku = await database.get(SkuORM, product.sku_id)
    if not sku:
        raise NotFoundError(detail="Sku of the product not found")
    
    return GetItemInfoResponse.model_validate(product)
