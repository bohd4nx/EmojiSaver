from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase

DATABASE_URL = "sqlite+aiosqlite:///./bot.db"

engine = create_async_engine(DATABASE_URL, echo=False)
SessionLocal = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


class Base(DeclarativeBase):
    pass


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def close_db():
    await engine.dispose()

# async def add(instance):
#     async with SessionLocal() as session:
#         try:
#             session.add(instance)
#             await session.commit()
#             await session.refresh(instance)
#             return instance
#         except IntegrityError:
#             await session.rollback()
#             return None
#         except Exception:
#             await session.rollback()
#             raise
