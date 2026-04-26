from uuid import UUID

from fastapi import APIRouter, Depends, Query

from app.dependencies.services.product import get_get_item_info_service
from app.services.product.get_item_info_service import GetItemInfoService
from app.services.product.dto.get_item_info import GetItemInfoResponse

router = APIRouter(tags=["SkuController"])


@router.get("/getItemInfo")
async def get_item_info(
    product_id: UUID = Query(
        ...,
        alias="id",
        description="UUIDv7 of the product"
    ),
    service: GetItemInfoService = Depends(get_get_item_info_service)
) -> GetItemInfoResponse:
    return await service.get_item_info(product_id=product_id)
