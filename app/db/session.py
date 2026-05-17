from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from app.core.config import settings


database_url = f"sqlite+aiosqlite:///{settings.sqlite_path}"

engine = create_async_engine(database_url, echo=False)
AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False)
