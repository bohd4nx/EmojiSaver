import logging
import os
from typing import Callable

from aiogram import Bot, Dispatcher, F, types
from aiogram.client.default import DefaultBotProperties
from aiogram.filters import Command
from pyrogram import Client

from data.config import config
from src.handlers import cmd_start, cmd_help, handle_emoji_message, handle_sticker_message
from src.utils import Messages

logging.getLogger('aiogram.dispatcher').setLevel(logging.INFO)
logging.getLogger('pyrogram').setLevel(logging.ERROR)


class EmojiDownloaderBot:
    def __init__(self) -> None:
        self.bot = Bot(
            token=config.BOT_TOKEN,
            default=DefaultBotProperties(parse_mode='HTML')
        )
        self.dp = Dispatcher()

        os.makedirs("data", exist_ok=True)
        self.pyro = Client(
            "data/session",
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            phone_number=config.PHONE_NUMBER,
            no_updates=True
        )

    async def start(self) -> None:
        try:
            await self._register_commands()
            self._register_handlers()
            await self.pyro.start()
            await self.dp.start_polling(self.bot)
        finally:
            await self.shutdown()

    async def shutdown(self) -> None:
        await self.pyro.stop()
        await self.bot.session.close()

    async def _register_commands(self) -> None:
        commands = [
            types.BotCommand(command="start", description="🚀 Start the bot"),
            types.BotCommand(command="help", description="❓ Show help information")
        ]
        await self.bot.set_my_commands(commands)

    def _register_handlers(self) -> None:
        self.dp.message.register(cmd_start, Command("start"))
        self.dp.message.register(cmd_help, Command("help"))

        self.dp.message.register(
            self._with_pyro(handle_emoji_message),
            F.entities.func(lambda entities: any(
                entity.type == "custom_emoji" for entity in entities
            ))
        )
        self.dp.message.register(
            self._with_pyro(handle_sticker_message),
            F.sticker
        )

        self.dp.message.register(self._handle_invalid_input)

    def _with_pyro(self, handler: Callable) -> Callable:
        async def wrapper(message: types.Message) -> None:
            await handler(message, self.pyro)

        return wrapper

    @staticmethod
    async def _handle_invalid_input(message: types.Message) -> None:

        await message.reply(Messages.INVALID_INPUT)
