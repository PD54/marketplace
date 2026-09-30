from fastapi import APIRouter, Depends

from app.dependencies.services.discount import get_create_discount_service
from app.services.discount.create_discount_service import CreateDiscountService
from app.services.discount.dto.create_discount import (
    CreateDiscountInputDTO,
    CreateDiscountOutputDTO,
)

router = APIRouter(tags=["DiscountApi"])


@router.post("/createDiscount")
async def create_discount(
    input_dto: CreateDiscountInputDTO,
    service: CreateDiscountService = Depends(get_create_discount_service),
) -> CreateDiscountOutputDTO:
    return await service.create_discount(input_dto)
