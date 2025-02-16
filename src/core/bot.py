import logging
import os
from typing import Any

from aiogram import Bot, Dispatcher, F, types
from aiogram.client.default import DefaultBotProperties
from aiogram.filters import Command
from pyrogram import Client

from data.config import config
from src.handlers import cmd_start, cmd_help, handle_emoji_message, handle_sticker_message
from src.utils import Messages

dispatcher_logger = logging.getLogger('aiogram.dispatcher')
dispatcher_logger.setLevel(logging.INFO)

pyrogram_logger = logging.getLogger('pyrogram')
pyrogram_logger.setLevel(logging.ERROR)


class EmojiDownloaderBot:
    def __init__(self) -> None:
        self.bot = Bot(token=config.BOT_TOKEN, default=DefaultBotProperties(parse_mode='HTML'))
        self.dp = Dispatcher()

        os.makedirs("data", exist_ok=True)
        self.pyro = Client(
            "data/session",
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            phone_number=config.PHONE_NUMBER,
            no_updates=True
        )

    def register_handlers(self) -> None:
        self.dp.message.register(cmd_start, Command("start"))
        self.dp.message.register(cmd_help, Command("help"))
        self.dp.message.register(
            self._create_emoji_wrapper(),
            F.entities.func(lambda entities: any(
                entity.type == "custom_emoji" for entity in entities
            ))
        )
        self.dp.message.register(self._create_sticker_wrapper(), F.sticker)
        self.dp.message.register(self._handle_invalid_input)

    @staticmethod
    async def _handle_invalid_input(message: types.Message) -> None:
        await message.reply(Messages.INVALID_INPUT)

    def _create_emoji_wrapper(self) -> Any:
        async def emoji_wrapper(message):
            await handle_emoji_message(message, self.pyro)

        return emoji_wrapper

    def _create_sticker_wrapper(self) -> Any:
        async def sticker_wrapper(message):
            await handle_sticker_message(message, self.pyro)

        return sticker_wrapper

    async def start(self) -> None:
        self.register_handlers()
        await self.pyro.start()
        try:
            await self.dp.start_polling(self.bot)
        finally:
            await self.shutdown()

    async def shutdown(self) -> None:
        await self.pyro.stop()
        await self.bot.session.close()
