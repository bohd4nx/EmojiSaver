import logging

from aiogram import Bot, Dispatcher, F, types
from aiogram.client.default import DefaultBotProperties
from aiogram.filters import Command

from app.handlers import cmd_start, cmd_help, handle_emoji, handle_sticker
from app.utils import MESSAGES
from .config import config

logging.getLogger('aiogram.dispatcher').setLevel(logging.INFO)


class TelegramBot:
    def __init__(self):
        self.bot = Bot(
            token=config["BOT_TOKEN"],
            default=DefaultBotProperties(parse_mode='HTML', link_preview_is_disabled=True)
        )
        self.dp = Dispatcher()

    async def setup(self):
        await self._register_commands()
        self._register_handlers()

    async def start_polling(self):
        await self.dp.start_polling(self.bot)

    async def close(self):
        await self.bot.session.close()

    async def _register_commands(self):
        commands = [
            types.BotCommand(command="start", description="🚀 Start the bot"),
            types.BotCommand(command="help", description="❓ Show help information")
        ]
        await self.bot.set_my_commands(commands)

    def _register_handlers(self):
        # Command handlers
        self.dp.message.register(cmd_start, Command("start"))
        self.dp.message.register(cmd_help, Command("help"))

        # Content handlers
        emoji_filter = F.entities.func(lambda entities: any(
            entity.type == "custom_emoji" for entity in entities
        ))
        self.dp.message.register(handle_emoji, emoji_filter)
        self.dp.message.register(handle_sticker, F.sticker)

        # Fallback handler
        self.dp.message.register(self._handle_invalid_input)

    @staticmethod
    async def _handle_invalid_input(message: types.Message):
        await message.reply(MESSAGES["invalid_input"])
