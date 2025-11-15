from aiogram import Dispatcher, types
from aiogram.filters import Command


async def cmd_help(message: types.Message, i18n):
    await message.answer(
        text=i18n.get("help-message")
    )


def register_help_handlers(dp: Dispatcher):
    dp.message.register(cmd_help, Command("help"))
