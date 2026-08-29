from fastapi import Depends

from app.database.repositories.good import GoodRepository
from app.database.repositories.sku import SkuRepository
from app.database.repositories.task import TaskRepository
from app.dependencies.repositories import (
    get_good_repository,
    get_sku_repository,
    get_task_repository,
)
from app.dependencies.services.task import get_replace_task_and_good_service
from app.services.good.get_item_info_service import GetItemInfoService
from app.services.good.move_to_not_found_service import MoveToNotFoundService
from app.services.task.replace_task_and_good import ReplaceTaskAndGoodService


def get_get_item_info_service(
    good_repo: GoodRepository = Depends(get_good_repository),
    sku_repo: SkuRepository = Depends(get_sku_repository),
) -> GetItemInfoService:
    return GetItemInfoService(good_repo=good_repo, sku_repo=sku_repo)


def get_move_to_not_found_service(
    good_repo: GoodRepository = Depends(get_good_repository),
    task_repo: TaskRepository = Depends(get_task_repository),
    replace_task_and_good_service: ReplaceTaskAndGoodService = Depends(
        get_replace_task_and_good_service,
    ),
) -> MoveToNotFoundService:
    return MoveToNotFoundService(
        good_repo=good_repo,
        task_repo=task_repo,
        replace_task_and_good_service=replace_task_and_good_service,
    )
