import logging
from typing import Callable

from aiogram import Bot, Dispatcher, F, types
from aiogram.client.default import DefaultBotProperties
from aiogram.filters import Command
from src.handlers import cmd_start, cmd_help, handle_emoji_message, handle_sticker_message
from src.utils import MESSAGES

from .config import config

logging.getLogger('aiogram.dispatcher').setLevel(logging.INFO)


class TelegramBot:
    def __init__(self) -> None:
        self.bot = Bot(
            token=config.BOT_TOKEN,
            default=DefaultBotProperties(parse_mode='HTML')
        )
        self.dp = Dispatcher()

    async def setup(self) -> None:
        await self._register_commands()
        self._register_handlers()

    async def start_polling(self) -> None:
        await self.dp.start_polling(self.bot)

    async def close(self) -> None:
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

        emoji_filter = F.entities.func(lambda entities: any(
            entity.type == "custom_emoji" for entity in entities
        ))
        self.dp.message.register(self._with_userbot(handle_emoji_message), emoji_filter)
        self.dp.message.register(self._with_userbot(handle_sticker_message), F.sticker)
        self.dp.message.register(self._handle_invalid_input)

    @staticmethod
    def _with_userbot(handler: Callable) -> Callable:
        async def wrapper(message: types.Message) -> None:
            from .app import app
            await handler(message, app.userbot.client)

        return wrapper

    @staticmethod
    async def _handle_invalid_input(message: types.Message) -> None:
        await message.reply(MESSAGES["invalid_input"])
