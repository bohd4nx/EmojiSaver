from aiogram import Dispatcher, types
from aiogram.filters import Command


async def cmd_start(message: types.Message, i18n):
    await message.answer(
        text=i18n.get("start-message", name=message.from_user.first_name)
    )


def register_start_handlers(dp: Dispatcher):
    dp.message.register(cmd_start, Command("start"))
