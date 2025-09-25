from aiogram import types

from app.utils import MESSAGES


async def cmd_start(message: types.Message) -> None:
    await message.answer(
        text=MESSAGES["start"].format(name=message.from_user.first_name)
    )


async def cmd_help(message: types.Message) -> None:
    await message.answer(
        text=MESSAGES["help"]
    )
