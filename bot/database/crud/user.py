from typing import Optional

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from ..models import User


class UserCRUD:
    @staticmethod
    async def get_or_create(
            session: AsyncSession,
            user_id: int,
            username: Optional[str] = None,
            full_name: Optional[str] = None
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
    async def get_by_id(session: AsyncSession, user_id: int) -> Optional[User]:
        result = await session.execute(select(User).where(User.user_id == user_id))
        return result.scalar_one_or_none()

    @staticmethod
    async def get_all(session: AsyncSession) -> list[User]:
        result = await session.execute(select(User))
        return list(result.scalars())
    
    @staticmethod
    async def increment_downloads(session: AsyncSession, user_id: int) -> None:
        user = await UserCRUD.get_by_id(session, user_id)
        if user:
            user.downloads += 1
            await session.commit()

    @staticmethod
    async def get_total_downloads(session: AsyncSession) -> int:
        result = await session.execute(select(func.sum(User.downloads)))
        total = result.scalar()
        return total if total else 0
