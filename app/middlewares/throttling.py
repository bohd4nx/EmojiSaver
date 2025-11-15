import time
from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import Message


class ThrottlingMiddleware(BaseMiddleware):
    def __init__(self, throttle_time: float):
        self.throttle_time = throttle_time
        self.user_timestamps: Dict[int, float] = {}

    async def __call__(
            self,
            handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
            event: Message,
            data: Dict[str, Any]
    ) -> Any:
        user_id = event.from_user.id
        current_time = time.time()

        if user_id in self.user_timestamps:
            time_passed = current_time - self.user_timestamps[user_id]

            if time_passed < self.throttle_time:
                wait_time = int(self.throttle_time - time_passed) + 1
                i18n = data["i18n"]
                await event.reply(i18n.get("throttle-warning", seconds=wait_time))
                return

        self.user_timestamps[user_id] = current_time
        return await handler(event, data)
