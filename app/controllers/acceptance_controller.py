from fastapi import APIRouter, Depends

from app.dependencies.services.acceptance import (
    get_create_acceptance_service,
)
from app.services.acceptance.create_acceptance_service import (
    CreateAcceptanceService,
)
from app.services.acceptance.dto.create_acceptance import (
    CreateAcceptanceInputDTO,
    CreateAcceptanceOutputDTO,
)

router = APIRouter(tags=["AcceptanceController"])


@router.post("/createAcceptance")
async def create_acceptance(
    input_dto: CreateAcceptanceInputDTO,
    service: CreateAcceptanceService = Depends(get_create_acceptance_service),
) -> CreateAcceptanceOutputDTO:
    return await service.create_acceptance(input_dto)
