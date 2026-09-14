from fastapi import Depends

from app.database.repositories.good import GoodRepository
from app.database.repositories.posting_good import PostingGoodRepository
from app.database.repositories.task import TaskRepository
from app.dependencies.repositories import (
    get_good_repository,
    get_posting_good_repository,
    get_task_repository,
)
from app.services.posting_good.pick_new_good_for_posting_service import (
    PickNewGoodForPostingService,
)


def get_pick_new_good_for_posting_service(
    good_repo: GoodRepository = Depends(get_good_repository),
    task_repo: TaskRepository = Depends(get_task_repository),
    posting_good_repo: PostingGoodRepository = Depends(
        get_posting_good_repository,
    ),
) -> PickNewGoodForPostingService:
    return PickNewGoodForPostingService(
        good_repo=good_repo,
        task_repo=task_repo,
        posting_good_repo=posting_good_repo,
    )
