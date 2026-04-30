from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.pydantic_schemas.responses.get_item_info import GetItemInfoResponse
from app.dependencies.session_generator import get_db
from app.exceptions.http_exceptions import NotFound
from app.models.product import Product

router = APIRouter(tags=["SkuController"])


@router.get("/getItemInfo", response_model=GetItemInfoResponse)
async def get_item_info(
    id: UUID,
    database: AsyncSession = Depends(get_db)
) -> GetItemInfoResponse:
    product = await database.get(Product, id)
    if not product:
        raise NotFound()
    
    return GetItemInfoResponse.model_validate(product)
