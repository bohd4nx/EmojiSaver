from contextlib import asynccontextmanager

from aiogram.types import Message
from aiogram_i18n import I18nContext


@asynccontextmanager
async def status_message(message: Message, i18n: I18nContext, processing_type: str = "processing", **kwargs):
    status_msg = await message.reply(i18n.get(processing_type, **kwargs))

    try:
        yield status_msg
    finally:
        try:
            await status_msg.delete()
        except Exception:
            pass
