from aiogram import Dispatcher, types


async def handle_invalid_input(message: types.Message, i18n):
    await message.reply(i18n.get("invalid-input"))


def register_fallback_handlers(dp: Dispatcher):
    dp.message.register(handle_invalid_input)
