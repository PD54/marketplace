from collections.abc import AsyncIterator

import pytest
from httpx import ASGITransport, AsyncClient

from main import app


@pytest.fixture
async def client(db_cleanup: None) -> AsyncIterator[AsyncClient]:
    transport = ASGITransport(app=app)
    async with AsyncClient(
        transport=transport,
        base_url="http://test",
    ) as client:
        yield client
