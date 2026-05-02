import os

from sqlalchemy import URL

POSTGRES_ADDR = os.getenv("POSTGRES_ADDR", "127.0.0.1")
port_str = os.getenv("POSTGRES_PORT", "5432")
POSTGRES_PORT = int(port_str) if port_str else None
POSTGRES_USER = os.getenv("POSTGRES_USER", "postgres")
POSTGRES_PASS = os.getenv("POSTGRES_PASSWORD", "1234")
POSTGRES_DB = os.getenv("POSTGRES_DB", "marketplace")

POSTGRES_URL = URL.create(
    drivername="postgresql+asyncpg",
    username=POSTGRES_USER,
    password=POSTGRES_PASS,
    host=POSTGRES_ADDR,
    port=POSTGRES_PORT,
    database=POSTGRES_DB
)
