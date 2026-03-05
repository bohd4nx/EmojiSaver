from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from bot.database.models import User


async def get_or_create_user(
        session: AsyncSession,
        user_id: int,
        username: str | None = None,
        full_name: str | None = None
) -> User:
    user = await get_user_by_id(session, user_id)
    if user:
        user.username = username
        user.full_name = full_name
    else:
        user = User(user_id=user_id, username=username, full_name=full_name)
        session.add(user)
    await session.commit()
    await session.refresh(user)
    return user


async def get_user_by_id(session: AsyncSession, user_id: int) -> User | None:
    result = await session.execute(select(User).where(User.user_id == user_id))
    return result.scalar_one_or_none()


async def get_all_users(session: AsyncSession) -> list[User]:
    result = await session.execute(select(User))
    return list(result.scalars())
