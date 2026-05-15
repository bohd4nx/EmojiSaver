from aiogram import Bot

from bot.core import logger
from bot.services import download_and_convert


async def process_all_emojis(emoji_ids: set[str], bot: Bot) -> tuple[dict[str, bytes], bool]:
    files: dict[str, bytes] = {}
    has_unsupported = False

    try:
        stickers = await bot.get_custom_emoji_stickers(list(emoji_ids))
    except Exception as exc:
        logger.error("Failed to fetch custom emoji stickers: %s", exc)
        return {}, False

    for sticker in stickers:
        try:
            emoji_files, is_unsupported = await download_and_convert(sticker.file_id, bot)
            files |= emoji_files
            has_unsupported = has_unsupported or is_unsupported
        except Exception as exc:
            logger.error("Failed to process emoji %s: %s", sticker.file_id, exc)

    return files, has_unsupported
