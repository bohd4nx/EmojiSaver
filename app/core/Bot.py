import logging

from aiogram import Bot, Dispatcher, F, types
from aiogram.client.default import DefaultBotProperties
from aiogram.filters import Command
from app.handlers import cmd_start, cmd_help, handle_emoji_message, handle_sticker_message
from app.utils import MESSAGES

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

        # Фильтр для сообщений с кастомными эмоджи
        emoji_filter = F.entities.func(lambda entities: any(
            entity.type == "custom_emoji" for entity in entities
        ))
        self.dp.message.register(handle_emoji_message, emoji_filter)

        # Фильтр для всех типов стикеров (анимированные, видео, статичные)
        self.dp.message.register(handle_sticker_message, F.sticker)

        # Обработчик для всех остальных сообщений
        self.dp.message.register(self._handle_invalid_input)

    async def _handle_invalid_input(self, message: types.Message) -> None:
        await message.reply(MESSAGES["invalid_input"])
