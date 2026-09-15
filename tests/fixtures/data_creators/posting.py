import pytest

from app.database.dto.posting import PostingDTO
from app.database.repositories.posting import PostingRepository


@pytest.fixture
async def posting_in_db(
    posting_repository: PostingRepository,
    posting: PostingDTO,
) -> PostingDTO:
    return await posting_repository.create(posting)
