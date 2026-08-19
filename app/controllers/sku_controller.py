from uuid import UUID

from fastapi import APIRouter, Depends, Query

from app.dependencies.services.good import get_get_item_info_service
from app.dependencies.services.sku import get_create_sku_service
from app.services.good.dto.get_item_info import GetItemInfoOutputDTO
from app.services.good.get_item_info_service import GetItemInfoService
from app.services.sku.create_sku_service import CreateSkuService
from app.services.sku.dto.create_sku import (
    CreateSkuInputDTO,
    CreateSkuOutputDTO,
)

router = APIRouter(tags=["SkuController"])


@router.get("/getItemInfo")
async def get_item_info(
    good_id: UUID = Query(
        ...,
        alias="id",
        description="Id of the good",
    ),
    service: GetItemInfoService = Depends(get_get_item_info_service),
) -> GetItemInfoOutputDTO:
    return await service.get_item_info(good_id=good_id)


@router.post("/createSku")
async def create_sku(
    input_dto: CreateSkuInputDTO,
    service: CreateSkuService = Depends(get_create_sku_service),
) -> CreateSkuOutputDTO:
    return await service.create_sku(input_dto)
