from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from bot.database.models import User


class UserCRUD:
    @staticmethod
    async def get_or_create(
            session: AsyncSession,
            user_id: int,
            username: str | None = None,
            full_name: str | None = None
    ) -> User:
        user = await UserCRUD.get_by_id(session, user_id)
        if user:
            user.username = username
            user.full_name = full_name
        else:
            user = User(user_id=user_id, username=username, full_name=full_name)
            session.add(user)
        await session.commit()
        await session.refresh(user)
        return user

    @staticmethod
    async def get_by_id(session: AsyncSession, user_id: int) -> User | None:
        result = await session.execute(select(User).where(User.user_id == user_id))
        return result.scalar_one_or_none()

    @staticmethod
    async def get_all(session: AsyncSession) -> list[User]:
        result = await session.execute(select(User))
        return list(result.scalars())
