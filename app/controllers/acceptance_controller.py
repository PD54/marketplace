from uuid import UUID

from fastapi import APIRouter, Depends, Query

from app.dependencies.services.acceptance import (
    get_create_acceptance_service,
    get_get_acceptance_info_service,
)
from app.services.acceptance.create_acceptance_service import (
    CreateAcceptanceService,
)
from app.services.acceptance.dto.create_acceptance import (
    CreateAcceptanceInputDTO,
    CreateAcceptanceOutputDTO,
)
from app.services.acceptance.dto.get_acceptance_info import (
    GetAcceptanceInfoOutputDTO,
)
from app.services.acceptance.get_acceptance_info_service import (
    GetAcceptanceInfoService,
)

router = APIRouter(tags=["AcceptanceController"])


@router.get("/getAcceptanceInfo")
async def get_acceptance_info(
    acceptance_id: UUID = Query(
        ...,
        alias="id",
        description="Id of the acceptance",
    ),
    service: GetAcceptanceInfoService = Depends(
        get_get_acceptance_info_service,
    ),
) -> GetAcceptanceInfoOutputDTO:
    return await service.get_acceptance_info(acceptance_id)


@router.post("/createAcceptance")
async def create_acceptance(
    input_dto: CreateAcceptanceInputDTO,
    service: CreateAcceptanceService = Depends(get_create_acceptance_service),
) -> CreateAcceptanceOutputDTO:
    return await service.create_acceptance(input_dto)
