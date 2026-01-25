import time
from collections.abc import Callable, Awaitable
from typing import Any

from aiogram import BaseMiddleware
from aiogram.types import CallbackQuery
from aiogram_i18n import I18nContext

from bot.core import config
from bot.utils import emoji


class RateLimitMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[CallbackQuery, dict[str, Any]], Awaitable[Any]],
            event: CallbackQuery,
            data: dict[str, Any]
    ) -> Any:
        wait_seconds = rate_limiter.check(event.from_user.id)

        if wait_seconds:
            i18n: I18nContext = data.get("i18n")
            await event.answer(
                i18n.get("rate-limit-alert", seconds=wait_seconds, forbidden=emoji['forbidden']),
                show_alert=True
            )
            return None

        return await handler(event, data)


class RateLimiter:
    def __init__(self):
        self.last_action: dict[int, float] = {}

    def check(self, user_id: int) -> int | None:
        current_time = time.time()
        time_passed = current_time - self.last_action.get(user_id, 0)

        if time_passed < config.RATE_LIMIT_COOLDOWN:
            return int(config.RATE_LIMIT_COOLDOWN - time_passed) + 1

        self.last_action[user_id] = current_time
        self._cleanup(current_time)
        return None

    def _cleanup(self, current_time: float) -> None:
        if len(self.last_action) > 100:
            expired = [uid for uid, t in self.last_action.items()
                       if current_time - t > config.RATE_LIMIT_COOLDOWN * 2]
            for uid in expired:
                del self.last_action[uid]


rate_limiter = RateLimiter()
