import pytest

from app.database.dto.posting import PostingDTO


@pytest.fixture
def posting() -> PostingDTO:
    return PostingDTO()
