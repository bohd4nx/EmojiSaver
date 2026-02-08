import time
from collections.abc import Callable, Awaitable
from typing import Any

from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery
from aiogram_i18n import I18nContext

from bot.core import config


class RateLimitMiddleware(BaseMiddleware):
    def __init__(self):
        super().__init__()
        self._users: dict[int, float] = {}

    async def __call__(
            self,
            handler: Callable[[Message | CallbackQuery, dict[str, Any]], Awaitable[Any]],
            event: Message | CallbackQuery,
            data: dict[str, Any]
    ) -> Any:
        user_id = event.from_user.id
        current_time = time.time()
        last_time = self._users.get(user_id, 0)
        time_passed = current_time - last_time

        if time_passed < config.RATE_LIMIT_COOLDOWN:
            wait_seconds = int(config.RATE_LIMIT_COOLDOWN - time_passed) + 1
            i18n: I18nContext = data.get("i18n")
            
            if isinstance(event, CallbackQuery):
                await event.answer(
                    i18n.get("rate-limit-alert", seconds=wait_seconds),
                    show_alert=True
                )
            else:
                await event.answer(i18n.get("rate-limit-alert", seconds=wait_seconds))
            return None

        self._users[user_id] = current_time
        self._cleanup(current_time)
        return await handler(event, data)

    def _cleanup(self, current_time: float) -> None:
        if len(self._users) > 100:
            self._users = {
                uid: t for uid, t in self._users.items()
                if current_time - t <= config.RATE_LIMIT_COOLDOWN * 2
            }
