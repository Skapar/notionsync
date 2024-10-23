from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from ..app.config import settings

async_engine = create_async_engine(
    settings.db.url.replace("sqlite://", "sqlite+aiosqlite://"), echo=settings.db.echo
)
AsyncSessionLocal = sessionmaker(
    bind=async_engine, class_=AsyncSession, expire_on_commit=False
)

sync_engine = create_engine(settings.db.url, echo=settings.db.echo)
SyncSessionLocal = sessionmaker(bind=sync_engine, autocommit=False, autoflush=False)


async def get_async_db():
    async with AsyncSessionLocal() as session:
        yield session


def get_sync_db():
    db = SyncSessionLocal()
    try:
        yield db
    finally:
        db.close()
