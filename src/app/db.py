from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from app.config import settings

sync_engine = create_engine(settings.url, echo=settings.echo)
SyncSessionLocal = sessionmaker(bind=sync_engine, autocommit=False, autoflush=False)

def get_sync_db():
    db = SyncSessionLocal()
    try:
        yield db
    finally:
        db.close()