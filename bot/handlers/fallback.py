from aiogram import Router
from aiogram.types import Message
from aiogram_i18n import I18nContext

router = Router(name=__name__)


@router.message()
async def handle_invalid_input(message: Message, i18n: I18nContext) -> None:
    await message.reply(i18n.get("help-message"))
