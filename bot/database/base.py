from pathlib import Path
from typing import Any

from sqlalchemy import event
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from bot.core.constants import DATABASE_FILE_NAME

DB_FILE = Path(__file__).parents[2] / DATABASE_FILE_NAME

engine = create_async_engine(f"sqlite+aiosqlite:///{DB_FILE}", echo=False)

SessionLocal = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


class Base(DeclarativeBase):
    pass


# Per-connection PRAGMAs: applied to every new connection from the pool.
# WAL is persisted at DB file level, but busy_timeout / synchronous / foreign_keys
# are connection-scoped and must be set here, not just once in init_db().
@event.listens_for(engine.sync_engine, "connect")
def _set_sqlite_pragma(dbapi_conn: Any, _connection_record: Any) -> None:
    cursor = dbapi_conn.cursor()
    cursor.execute("PRAGMA journal_mode=WAL")
    cursor.execute("PRAGMA busy_timeout=60000")
    cursor.execute("PRAGMA synchronous=NORMAL")
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()


async def init_db() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def close_db() -> None:
    await engine.dispose()
