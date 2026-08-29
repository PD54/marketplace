import pytest

from app.database.dto.acceptance import AcceptanceDTO


@pytest.fixture
def acceptance() -> AcceptanceDTO:
    return AcceptanceDTO()
