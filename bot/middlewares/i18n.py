from typing import Any, Awaitable, Callable, Dict, Optional

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from aiogram_i18n import I18nContext


class LocaleMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any],
    ) -> Any:
        i18n: Optional[I18nContext] = data.get("i18n")
        user = getattr(event, "from_user", None)

        if i18n and user:
            try:
                locale = user.language_code if user.language_code in ["en", "ru"] else "en"
                await i18n.set_locale(locale)
            except Exception:
                pass

        return await handler(event, data)


__all__ = ["LocaleMiddleware"]
