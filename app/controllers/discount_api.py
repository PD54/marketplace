from fastapi import APIRouter, Depends, Response, status

from app.dependencies.services.discount import (
    get_cancel_discount_service,
    get_create_discount_service,
)
from app.services.discount.cancel_discount_service import CancelDiscountService
from app.services.discount.create_discount_service import CreateDiscountService
from app.services.discount.dto.cancel_discount import CancelDiscountInputDTO
from app.services.discount.dto.create_discount import (
    CreateDiscountInputDTO,
    CreateDiscountOutputDTO,
)

router = APIRouter(tags=["DiscountApi"])


@router.post("/cancelDiscount")
async def cancel_discount(
    input_dto: CancelDiscountInputDTO,
    service: CancelDiscountService = Depends(get_cancel_discount_service),
) -> Response:
    await service.cancel_discount(input_dto)
    return Response(status_code=status.HTTP_200_OK)


@router.post("/createDiscount")
async def create_discount(
    input_dto: CreateDiscountInputDTO,
    service: CreateDiscountService = Depends(get_create_discount_service),
) -> CreateDiscountOutputDTO:
    return await service.create_discount(input_dto)
