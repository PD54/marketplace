import pytest

from app.database.dto.acceptance import AcceptanceDTO
from app.database.repositories.acceptance import AcceptanceRepository


@pytest.fixture
async def acceptance_in_db(
    acceptance_repository: AcceptanceRepository,
    acceptance: AcceptanceDTO,
) -> AcceptanceDTO:
    return await acceptance_repository.create(acceptance)
