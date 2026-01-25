from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram_i18n import I18nContext

from bot.__meta__ import GITHUB_URL, DEVELOPER_URL
from bot.database import SessionLocal
from bot.database.crud import DownloadsCRUD
from bot.utils import escape_html, emoji

router = Router(name=__name__)


@router.message(CommandStart())
async def start_command(message: Message, i18n: I18nContext) -> None:
    async with SessionLocal() as session:
        total_downloads = await DownloadsCRUD.get_total_downloads(session)

    await message.answer(
        i18n.get(
            "start-message",
            name=escape_html(message.from_user.first_name),
            github_link=GITHUB_URL,
            developer=DEVELOPER_URL,
            downloads=total_downloads,
            hello=emoji['hello'],
            convert=emoji['convert'],
            download=emoji['download'],
            search=emoji['search'],
            github=emoji['github'],
            telegram=emoji['telegram']
        )
    )
