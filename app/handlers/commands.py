from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder

from src.utils import MESSAGES


def _get_keyboard() -> InlineKeyboardBuilder:
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text="⭐️ GitHub", url="https://github.com/bohd4nx/EmojiSaver")
    keyboard.button(text="👨‍💻 Developer", url="https://t.me/bohd4nx")
    keyboard.adjust(2)
    return keyboard


async def cmd_start(message: types.Message) -> None:
    await message.answer(
        text=MESSAGES["start"].format(name=message.from_user.first_name),
        reply_markup=_get_keyboard().as_markup()
    )


async def cmd_help(message: types.Message) -> None:
    await message.answer(
        text=MESSAGES["help"],
        reply_markup=_get_keyboard().as_markup()
    )
