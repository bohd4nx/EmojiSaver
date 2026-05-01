from collections.abc import Awaitable, Callable
from typing import TYPE_CHECKING, Any

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject

from bot.core import logger
from bot.core.constants import DEFAULT_LOCALE, SUPPORTED_LOCALES

if TYPE_CHECKING:
    from aiogram_i18n import I18nContext


class LocaleMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Any:
        i18n: I18nContext | None = data.get("i18n")
        user = data.get("event_from_user")

        if i18n and user:
            try:
                # user may have unsupported language codes, so we normalize to the default locale.
                locale = user.language_code if user.language_code in SUPPORTED_LOCALES else DEFAULT_LOCALE
                await i18n.set_locale(locale)
            except Exception as exc:
                logger.debug("Failed to set locale for user %s: %s", user.id, exc)

        return await handler(event, data)
