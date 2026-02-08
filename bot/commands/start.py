from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram_i18n import I18nContext

from bot.database import SessionLocal
from bot.database.crud import DownloadsCRUD
from bot.utils import escape_html

router = Router(name=__name__)


@router.message(CommandStart())
async def start_command(message: Message, i18n: I18nContext) -> None:
    async with SessionLocal() as session:
        total_downloads = await DownloadsCRUD.get_total_downloads(session)

    await message.answer(
        i18n.get(
            "start-message",
            name=escape_html(message.from_user.first_name),
            downloads=total_downloads
        )
    )
