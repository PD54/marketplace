from fastapi import Depends

from app.database.repositories.acceptance import AcceptanceRepository
from app.database.repositories.sku import SkuRepository
from app.database.repositories.task import TaskRepository
from app.dependencies.repositories import (
    get_acceptance_repository,
    get_sku_repository,
    get_task_repository,
)
from app.services.acceptance.create_acceptance_service import (
    CreateAcceptanceService,
)
from app.services.acceptance.get_acceptance_info_service import (
    GetAcceptanceInfoService,
)


def get_create_acceptance_service(
    acceptance_repo: AcceptanceRepository = Depends(
        get_acceptance_repository,
    ),
    sku_repo: SkuRepository = Depends(get_sku_repository),
    task_repo: TaskRepository = Depends(get_task_repository),
) -> CreateAcceptanceService:
    return CreateAcceptanceService(
        acceptance_repo=acceptance_repo,
        sku_repo=sku_repo,
        task_repo=task_repo,
    )


def get_get_acceptance_info_service(
    acceptance_repo: AcceptanceRepository = Depends(
        get_acceptance_repository,
    ),
    task_repo: TaskRepository = Depends(get_task_repository),
) -> GetAcceptanceInfoService:
    return GetAcceptanceInfoService(
        acceptance_repo=acceptance_repo,
        task_repo=task_repo,
    )
