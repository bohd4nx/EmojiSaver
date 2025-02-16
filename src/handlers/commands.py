from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder

from src.utils import Messages, Buttons


def _get_keyboard() -> InlineKeyboardBuilder:
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text=Buttons.GITHUB, url=Buttons.GITHUB_URL)
    keyboard.button(text=Buttons.DEVELOPER, url=Buttons.DEVELOPER_URL)
    keyboard.adjust(2)
    return keyboard


async def cmd_start(message: types.Message) -> None:
    await message.delete()
    name = message.from_user.first_name
    await message.answer(
        text=Messages.START.format(name=name),
        reply_markup=_get_keyboard().as_markup()
    )


async def cmd_help(message: types.Message) -> None:
    await message.delete()
    await message.answer(
        text=Messages.HELP,
        reply_markup=_get_keyboard().as_markup()
    )
