from fastapi import Depends

from app.database.repositories.good import GoodRepository
from app.database.repositories.task import TaskRepository
from app.dependencies.repositories import (
    get_good_repository,
    get_task_repository,
)
from app.services.task.replace_task_and_good import ReplaceTaskAndGoodService


def get_replace_task_and_good_service(
    good_repo: GoodRepository = Depends(get_good_repository),
    task_repo: TaskRepository = Depends(get_task_repository),
) -> ReplaceTaskAndGoodService:
    return ReplaceTaskAndGoodService(
        good_repo=good_repo,
        task_repo=task_repo,
    )
