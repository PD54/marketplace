import pytest

from app.database.dto.good import GoodDTO
from app.database.dto.posting_good import PostingGoodDTO
from app.database.repositories.good import GoodRepository
from app.database.repositories.posting_good import PostingGoodRepository
from app.database.repositories.task import TaskRepository
from app.services.posting_good.pick_new_good_for_posting_service import (
    PickNewGoodForPostingService,
)


@pytest.fixture
def pick_new_good_for_posting_service(
    good_repository: GoodRepository,
    task_repository: TaskRepository,
    posting_good_repository: PostingGoodRepository,
) -> PickNewGoodForPostingService:
    return PickNewGoodForPostingService(
        good_repo=good_repository,
        task_repo=task_repository,
        posting_good_repo=posting_good_repository,
    )


async def test_pick_new_good_for_posting_success(
    posting_good_in_db: PostingGoodDTO,
    good_in_db: GoodDTO,
    pick_new_good_for_posting_service: PickNewGoodForPostingService,
    posting_good_repository: PostingGoodRepository,
    task_repository: TaskRepository,
    good_repository: GoodRepository,
):
    result = await pick_new_good_for_posting_service.pick_new_good(
        posting_good_in_db,
    )

    new_good = await good_repository.get_by_id(result.good_id)
    posting_goods_with_new_good = await posting_good_repository.get_by_good_id(
        new_good.id,
    )
    tasks_with_new_good = await task_repository.get_by_good_id(new_good.id)

    assert new_good.id == good_in_db.id
    assert new_good.sku_id == posting_good_in_db.good_sku_id
    assert new_good.stock == posting_good_in_db.good_stock
    assert new_good.reserved_state is True

    assert len(posting_goods_with_new_good) == 1
    assert posting_goods_with_new_good[0].good_id == good_in_db.id
    assert (
        posting_goods_with_new_good[0].posting_id
        == posting_good_in_db.posting_id
    )
    assert posting_goods_with_new_good[0] == result

    assert len(tasks_with_new_good) == 1
    assert tasks_with_new_good[0].good_id == good_in_db.id
    assert tasks_with_new_good[0].posting_id == posting_good_in_db.posting_id


async def test_pick_new_good_for_posting_good_not_found(
    reserved_good_in_db: GoodDTO,
    posting_good_in_db: PostingGoodDTO,
    pick_new_good_for_posting_service: PickNewGoodForPostingService,
):
    result = await pick_new_good_for_posting_service.pick_new_good(
        posting_good_in_db
    )

    assert result is None
