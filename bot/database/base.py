import os

from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase

from bot.__meta__ import APP_NAME

DATABASE_URL = os.getenv("DATABASE_URL", f"sqlite+aiosqlite:///./{APP_NAME}.db")

if "sqlite" in DATABASE_URL:
    engine = create_async_engine(
        DATABASE_URL,
        echo=False,
        connect_args={
            "check_same_thread": False,
            "timeout": 60,
        }
    )
else:
    engine = create_async_engine(
        DATABASE_URL,
        echo=False,
        pool_size=50,
        max_overflow=100,
        pool_pre_ping=True,
        pool_recycle=3600,
    )

SessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False
)


class Base(DeclarativeBase):
    pass


async def init_db():
    async with engine.begin() as conn:
        if "sqlite" in DATABASE_URL:
            await conn.execute(text("PRAGMA journal_mode=WAL"))
            await conn.execute(text("PRAGMA busy_timeout=60000"))
            await conn.execute(text("PRAGMA synchronous=NORMAL"))
            await conn.execute(text("PRAGMA foreign_keys=ON"))
        await conn.run_sync(Base.metadata.create_all)


async def close_db():
    await engine.dispose()
