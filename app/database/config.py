import os


POSTGRES_ADDR = os.getenv("POSTGRES_ADDR", "127.0.0.1")
POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5432")
POSTGRES_USER = os.getenv("POSTGRES_USER", "postgres")
POSTGRES_PASS = os.getenv("POSTGRES_PASSWORD", "postgres")
POSTGRES_DB = os.getenv("POSTGRES_DB", "marketplace")


def create_connection_url(
    pg_addr: str,
    pg_port: str,
    pg_user: str,
    pg_pass: str,
    pg_db: str
) -> str:
    return (
        f"postgresql+asyncpg://"
        f"{pg_user}:{pg_pass}@{pg_addr}:{pg_port}/{pg_db}"
    )


POSTGRES_URL = create_connection_url(
    pg_addr=POSTGRES_ADDR,
    pg_port=POSTGRES_PORT,
    pg_user=POSTGRES_USER,
    pg_pass=POSTGRES_PASS,
    pg_db=POSTGRES_DB
)
