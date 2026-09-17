from uuid import UUID

from fastapi import APIRouter, Depends, Query, Response, status

from app.dependencies.services.good import (
    get_get_item_info_service,
    get_move_to_not_found_service,
)
from app.dependencies.services.sku import (
    get_create_sku_service,
    get_toggle_is_hidden_service,
)
from app.services.good.dto.get_item_info import GetItemInfoOutputDTO
from app.services.good.dto.move_to_not_found import MoveToNotFoundInputDTO
from app.services.good.get_item_info_service import GetItemInfoService
from app.services.good.move_to_not_found_service import MoveToNotFoundService
from app.services.sku.create_sku_service import CreateSkuService
from app.services.sku.dto.create_sku import (
    CreateSkuInputDTO,
    CreateSkuOutputDTO,
)
from app.services.sku.dto.toggle_is_hidden import ToggleIsHiddenInputDTO
from app.services.sku.toggle_is_hidden import ToggleIsHiddenService

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


@router.post("/toggleIsHidden")
async def toggle_is_hidden(
    input_dto: ToggleIsHiddenInputDTO,
    service: ToggleIsHiddenService = Depends(get_toggle_is_hidden_service),
) -> Response:
    await service.toggle_is_hidden(input_dto)
    return Response(status_code=status.HTTP_200_OK)


@router.post("/moveToNotFound")
async def move_to_not_found(
    input_dto: MoveToNotFoundInputDTO,
    service: MoveToNotFoundService = Depends(get_move_to_not_found_service),
) -> Response:
    await service.move_to_not_found(input_dto)
    return Response(status_code=status.HTTP_200_OK)
