from sqlalchemy import func, select
from sqlalchemy.dialects.sqlite import insert
from sqlalchemy.ext.asyncio import AsyncSession

from bot.database.models import User


async def get_user(session: AsyncSession, user_id: int) -> User | None:
    result = await session.execute(select(User).where(User.user_id == user_id))
    return result.scalar_one_or_none()


async def get_or_create_user(
    session: AsyncSession,
    user_id: int,
    username: str | None = None,
) -> User:
    base_stmt = insert(User).values(
        user_id=user_id,
        username=username,
    )
    stmt = base_stmt.on_conflict_do_update(
        index_elements=["user_id"],
        set_={
            "username": base_stmt.excluded.username,
            "updated_at": func.now(),
        },
    ).returning(User)
    user = (await session.scalars(stmt)).one()
    await session.commit()
    await session.refresh(user)
    return user


async def get_all_users(session: AsyncSession) -> list[User]:
    result = await session.execute(select(User))
    return list(result.scalars())
