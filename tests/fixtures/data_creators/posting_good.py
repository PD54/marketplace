import pytest

from app.database.dto.good import GoodDTO
from app.database.dto.posting import PostingDTO
from app.database.dto.posting_good import PostingGoodDTO
from app.database.repositories.posting_good import PostingGoodRepository


@pytest.fixture
async def posting_good_in_db(
    posting_good_repository: PostingGoodRepository,
    posting_good: PostingGoodDTO,
    posting_in_db: PostingDTO,
    good_reserved_in_db: GoodDTO,
) -> PostingGoodDTO:
    return await posting_good_repository.create(posting_good)
