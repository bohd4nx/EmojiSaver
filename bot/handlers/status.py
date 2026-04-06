from collections.abc import AsyncIterator
from contextlib import asynccontextmanager, suppress
from typing import Any

from aiogram.types import Message
from aiogram_i18n import I18nContext


@asynccontextmanager
async def status_message(
    message: Message,
    i18n: I18nContext,
    processing_type: str = "processing",
    **format_kwargs: Any,
) -> AsyncIterator[Message]:
    """Send temporary status text and delete it after the context finishes."""
    status_text = i18n.get(processing_type, **format_kwargs)
    status_msg = await message.reply(status_text)

    try:
        yield status_msg
    finally:
        with suppress(Exception):
            await status_msg.delete()
