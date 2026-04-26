from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from app.database.config import POSTGRES_URL


async_engine = create_async_engine(url=POSTGRES_URL, echo=True)
async_session = async_sessionmaker(async_engine)