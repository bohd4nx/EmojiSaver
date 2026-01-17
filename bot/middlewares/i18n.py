from collections.abc import Awaitable, Callable
from typing import Any

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from aiogram_i18n import I18nContext


class LocaleMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: dict[str, Any],
    ) -> Any:
        i18n: I18nContext | None = data.get("i18n")
        user = getattr(event, "from_user", None)

        if i18n and user:
            try:
                locale = user.language_code if user.language_code in ["en", "ru"] else "en"
                await i18n.set_locale(locale)
            except Exception:
                pass

        return await handler(event, data)


__all__ = ["LocaleMiddleware"]
