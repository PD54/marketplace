import os
import sys

from pydantic_settings import BaseSettings
from sqlalchemy import URL
from sqlalchemy.pool import NullPool


class DatabaseSettings(BaseSettings):
    postgres_addr: str = "127.0.0.1"
    postgres_port: int = 5432
    postgres_user: str = "postgres"
    postgres_password: str = "postgres"
    postgres_db: str = "marketplace"
    db_echo: bool = False

    @property
    def is_test_mode(self) -> bool:
        return "pytest" in sys.argv[0] or "PYTEST_XDIST_WORKER" in os.environ

    @property
    def db_name(self) -> str:
        if not self.is_test_mode:
            return self.postgres_db

        worker = os.environ.get("PYTEST_XDIST_WORKER", "gw0")
        return f"test_{self.postgres_db}_{worker}"

    @property
    def database_url(self) -> str:
        return URL.create(
            drivername="postgresql+asyncpg",
            username=self.postgres_user,
            password=self.postgres_password,
            host=self.postgres_addr,
            port=self.postgres_port,
            database=self.db_name,
        ).render_as_string(hide_password=False)

    @property
    def pool_class(self) -> type[NullPool] | None:
        return NullPool if self.is_test_mode else None


database_settings = DatabaseSettings()
