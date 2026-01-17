from datetime import datetime

from sqlalchemy import String, DateTime, func, BigInteger, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from bot.database.base import Base


class User(Base):
    __tablename__ = "users"

    user_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    username: Mapped[str | None] = mapped_column(String(255), nullable=True, index=True)
    full_name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now(), index=True)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=func.now(), onupdate=func.now())

    downloads: Mapped[list["Download"]] = relationship(
        "Download",
        back_populates="user",
        cascade="all, delete-orphan"
    )


class Download(Base):
    __tablename__ = "downloads"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False, index=True)
    content_type: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    content_id: Mapped[str | None] = mapped_column(String(255), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now(), nullable=False, index=True)

    user: Mapped["User"] = relationship("User", back_populates="downloads")
