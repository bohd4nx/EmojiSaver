from aiogram import Bot
from aiogram.types import BotCommand

# bot commands shown in the Telegram menu, keyed by language code
COMMANDS: dict[str, list[BotCommand]] = {
    "ru": [
        BotCommand(command="start", description="🏠 Главное меню"),
        BotCommand(command="help", description="❓ Помощь"),
    ],
    "en": [
        BotCommand(command="start", description="🏠 Main menu"),
        BotCommand(command="help", description="❓ Help"),
    ],
}

# full bot description shown on the profile page
DESCRIPTIONS: dict[str, str] = {
    "ru": (
        "Скачивайте и конвертируйте стикеры и анимированные эмодзи Telegram в форматы TGS, JSON, Lottie и PNG.\n\n"
        "Извлекайте кастомные эмодзи, конвертируйте стикеры и скачивайте целые паки."
    ),
    "en": (
        "Download and convert Telegram animated emoji & stickers to TGS, JSON, Lottie, and PNG formats.\n\n"
        "Extract custom emoji, convert stickers, and download entire packs."
    ),
}

# short description shown in search results and sharing cards
SHORT_DESCRIPTIONS: dict[str, str] = {
    "ru": "🔄 Конвертируйте и скачивайте анимированные эмодзи и стикеры Telegram",
    "en": "🔄 Download and convert Telegram animated emoji & stickers to editable formats",
}


async def setup_bot_profile(bot: Bot) -> None:
    """Push commands, description and short description to Telegram for all locales."""
    for lang, cmds in COMMANDS.items():
        await bot.set_my_commands(cmds, language_code=lang)

    for lang, desc in DESCRIPTIONS.items():
        await bot.set_my_description(desc, language_code=lang)

    for lang, short_desc in SHORT_DESCRIPTIONS.items():
        await bot.set_my_short_description(short_desc, language_code=lang)
