from collections.abc import AsyncIterator, Iterator

import pytest
from alembic import command
from alembic.config import Config
from sqlalchemy import text
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from app.config.database_settings import database_settings
from app.database.orm_models.base import BaseORM


@pytest.fixture(scope="session")
async def setup_test_database() -> AsyncIterator[None]:
    test_db_name = database_settings.db_name
    root_url = database_settings.database_url.replace(
        test_db_name,
        "postgres",
    )
    root_engine = create_async_engine(
        root_url,
        isolation_level="AUTOCOMMIT",
    )

    async with root_engine.connect() as connection:
        await connection.execute(
            text(f"DROP DATABASE IF EXISTS {test_db_name} WITH (FORCE)")
        )
        await connection.execute(text(f"CREATE DATABASE {test_db_name}"))
    await root_engine.dispose()

    yield

    root_engine = create_async_engine(
        root_url,
        isolation_level="AUTOCOMMIT",
    )

    async with root_engine.connect() as connection:
        await connection.execute(
            text(f"DROP DATABASE IF EXISTS {test_db_name} WITH (FORCE)"),
        )
    await root_engine.dispose()


@pytest.fixture(scope="session")
def run_migrations(setup_test_database: None) -> Iterator[None]:
    alembic_config = Config("alembic.ini")
    command.upgrade(alembic_config, "head")

    yield

    command.downgrade(alembic_config, "base")


@pytest.fixture(scope="session")
async def test_engine() -> AsyncIterator[AsyncEngine]:
    engine = create_async_engine(
        url=database_settings.database_url,
        echo=database_settings.db_echo,
        poolclass=database_settings.pool_class,
        isolation_level="AUTOCOMMIT",
    )

    yield engine

    await engine.dispose()


@pytest.fixture
async def db_cleanup(
    test_engine: AsyncEngine,
    run_migrations: None,
) -> AsyncIterator[None]:
    yield

    tables = [table.name for table in reversed(BaseORM.metadata.sorted_tables)]

    async with test_engine.connect() as connection:
        for table in tables:
            await connection.execute(text(f"DELETE FROM {table}"))


@pytest.fixture
async def db_session(
    test_engine: AsyncEngine,
    db_cleanup: None,
) -> AsyncIterator[AsyncSession]:
    test_async_session = async_sessionmaker(test_engine)

    async with test_async_session() as session:
        yield session
