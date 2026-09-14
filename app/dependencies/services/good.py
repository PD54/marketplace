from fastapi import Depends

from app.database.repositories.good import GoodRepository
from app.database.repositories.posting_good import PostingGoodRepository
from app.database.repositories.sku import SkuRepository
from app.database.repositories.task import TaskRepository
from app.dependencies.repositories import (
    get_good_repository,
    get_posting_good_repository,
    get_sku_repository,
    get_task_repository,
)
from app.dependencies.services.posting_good import (
    get_pick_new_good_for_posting_service,
)
from app.services.good.get_item_info_service import GetItemInfoService
from app.services.good.move_to_not_found_service import MoveToNotFoundService
from app.services.posting_good.pick_new_good_for_posting_service import (
    PickNewGoodForPostingService,
)


def get_get_item_info_service(
    good_repo: GoodRepository = Depends(get_good_repository),
    sku_repo: SkuRepository = Depends(get_sku_repository),
) -> GetItemInfoService:
    return GetItemInfoService(good_repo=good_repo, sku_repo=sku_repo)


def get_move_to_not_found_service(
    good_repo: GoodRepository = Depends(get_good_repository),
    task_repo: TaskRepository = Depends(get_task_repository),
    posting_good_repo: PostingGoodRepository = Depends(
        get_posting_good_repository,
    ),
    pick_new_good_for_posting_service: PickNewGoodForPostingService = Depends(
        get_pick_new_good_for_posting_service,
    ),
) -> MoveToNotFoundService:
    return MoveToNotFoundService(
        good_repo=good_repo,
        task_repo=task_repo,
        posting_good_repo=posting_good_repo,
        pick_new_good_for_posting_service=pick_new_good_for_posting_service,
    )
