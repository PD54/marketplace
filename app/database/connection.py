from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from app.config.database_settings import database_settings

async_engine = create_async_engine(
    url=database_settings.database_url,
    echo=database_settings.db_echo,
    poolclass=database_settings.pool_class
)
async_session = async_sessionmaker(async_engine)
