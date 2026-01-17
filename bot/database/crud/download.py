from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from bot.database.models import Download


class DownloadsCRUD:
    @staticmethod
    async def add_download(
            session: AsyncSession,
            user_id: int,
            content_type: str,
            content_id: str | None = None
    ) -> Download:
        download = Download(
            user_id=user_id,
            content_type=content_type,
            content_id=content_id
        )
        session.add(download)
        await session.commit()
        await session.refresh(download)
        return download

    @staticmethod
    async def get_by_id(session: AsyncSession, download_id: int) -> Download | None:
        result = await session.execute(select(Download).where(Download.id == download_id))
        return result.scalar_one_or_none()

    @staticmethod
    async def get_user_downloads(
            session: AsyncSession,
            user_id: int,
            limit: int | None = None
    ) -> list[Download]:
        query = select(Download).where(Download.user_id == user_id).order_by(Download.created_at.desc())

        if limit:
            query = query.limit(limit)

        result = await session.execute(query)
        return list(result.scalars())

    @staticmethod
    async def get_total_downloads(session: AsyncSession) -> int:
        result = await session.execute(select(func.count(Download.id)))
        return result.scalar() or 0
