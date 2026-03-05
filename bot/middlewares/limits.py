from collections.abc import Awaitable, Callable
import time
from typing import TYPE_CHECKING, Any

from aiogram import BaseMiddleware
from aiogram.types import CallbackQuery, TelegramObject

from bot.core import config

if TYPE_CHECKING:
    from aiogram_i18n import I18nContext


class RateLimitMiddleware(BaseMiddleware):
    def __init__(self) -> None:
        super().__init__()
        self._users: dict[int, float] = {}

    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Any:
        user = data.get("event_from_user")
        if not user:
            return await handler(event, data)

        now = time.monotonic()
        elapsed = now - self._users.get(user.id, 0.0)

        if elapsed < config.RATE_LIMIT_COOLDOWN:
            wait = int(config.RATE_LIMIT_COOLDOWN - elapsed) + 1
            i18n: I18nContext = data["i18n"]
            text = i18n.get("rate-limit-alert", seconds=wait)

            if isinstance(event, CallbackQuery):
                await event.answer(text, show_alert=True)
            else:
                await event.answer(text)
            return None

        self._users[user.id] = now
        self._cleanup(now)
        return await handler(event, data)

    def _cleanup(self, now: float) -> None:
        if len(self._users) > 100:
            cutoff = now - config.RATE_LIMIT_COOLDOWN * 2
            self._users = {uid: t for uid, t in self._users.items() if t > cutoff}
