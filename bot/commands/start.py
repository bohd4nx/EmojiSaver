from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram_i18n import I18nContext

from bot import __meta__
from bot.database import SessionLocal
from bot.database.crud import UserCRUD
from bot.utils import escape_html

router = Router(name=__name__)


@router.message(CommandStart())
async def start_command(message: Message, i18n: I18nContext) -> None:
    user = message.from_user

    async with SessionLocal() as session:
        await UserCRUD.get_or_create(
            session=session,
            user_id=user.id,
            username=user.username,
            full_name=user.full_name
        )

        total_downloads = await UserCRUD.get_total_downloads(session)

    await message.answer(
        i18n.get(
            "start-message",
            name=escape_html(user.first_name),
            github=__meta__.__github__,
            developer=__meta__.__developer__,
            downloads=total_downloads
        )
    )
