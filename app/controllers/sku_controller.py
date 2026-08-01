from uuid import UUID

from fastapi import APIRouter, Depends, Query

from app.dependencies.services.product import get_get_item_info_service
from app.dependencies.services.sku import get_create_sku_service
from app.services.product.get_item_info_service import GetItemInfoService
from app.services.product.dto.get_item_info import GetItemInfoOutputDTO
from app.services.sku.create_sku_service import CreateSkuService
from app.services.sku.dto.create_sku import (
    CreateSkuInputDTO,
    CreateSkuOutputDTO
)

router = APIRouter(tags=["SkuController"])


@router.get("/getItemInfo")
async def get_item_info(
    product_id: UUID = Query(
        ...,
        alias="id",
        description="UUIDv7 of the product"
    ),
    service: GetItemInfoService = Depends(get_get_item_info_service)
) -> GetItemInfoOutputDTO:
    return await service.get_item_info(product_id=product_id)


@router.post("/createSku")
async def create_sku(
    input_dto: CreateSkuInputDTO,
    service: CreateSkuService = Depends(get_create_sku_service)
) -> CreateSkuOutputDTO:
    return await service.create_sku(input_dto)
