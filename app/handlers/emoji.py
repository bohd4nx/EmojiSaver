from typing import Dict, Set

from aiogram import Dispatcher, F, types

from app.core import logger
from app.utils import download_and_convert, send_result, pack_zip


async def handle_emoji(message: types.Message, i18n):
    emoji_ids = {entity.custom_emoji_id for entity in message.entities
                 if entity.type == "custom_emoji"}

    logger.debug(f"Detected emoji IDs: {emoji_ids}")

    if not emoji_ids:
        await message.reply(i18n.get("no-emoji"))
        return

    status_message = await message.reply(i18n.get("loading"))

    try:
        files, has_unsupported = await process_all_emojis(emoji_ids, message.bot)
        await handle_result(message, status_message, files, has_unsupported, i18n)
    except Exception as e:
        logger.exception(f"Error handling emoji: {e}")
        await status_message.edit_text(i18n.get("error", error=str(e)))


async def process_all_emojis(emoji_ids: Set[str], bot) -> tuple[Dict[str, bytes], bool]:
    files = {}
    has_unsupported = False

    for emoji_id in emoji_ids:
        logger.debug(f"Processing emoji: {emoji_id}")
        try:
            emoji_files, is_unsupported = await process_emoji(emoji_id, bot)
            logger.debug(f"Emoji {emoji_id} processed: {len(emoji_files)} files, unsupported={is_unsupported}")
            files.update(emoji_files)
            if is_unsupported:
                has_unsupported = True
        except Exception as e:
            logger.exception(f"Error processing emoji {emoji_id}: {e}")

    return files, has_unsupported


async def process_emoji(emoji_id: str, bot) -> tuple[Dict[str, bytes], bool]:
    try:
        logger.debug(f"Getting custom emoji stickers for: {emoji_id}")
        stickers = await bot.get_custom_emoji_stickers([emoji_id])

        if not stickers:
            logger.warning(f"No stickers found for emoji: {emoji_id}")
            return {}, False

        emoji = stickers[0]
        logger.debug(f"Emoji file_id: {emoji.file_id}")

        return await download_and_convert(emoji.file_id, bot)
    except Exception as e:
        logger.exception(f"Failed to process emoji {emoji_id}: {e}")
        return {}, False


async def handle_result(message: types.Message, status_message: types.Message,
                        files: Dict[str, bytes], has_unsupported: bool, i18n):
    if not files:
        logger.warning("No files to send")
        await status_message.edit_text(i18n.get("processing-failed"))
        return

    logger.debug(f"Packing {len(files)} files into archive")
    archive_data = await pack_zip(files)
    logger.debug(f"Archive created: {len(archive_data)} bytes")

    caption = i18n.get("format-warning") if has_unsupported else None
    await send_result(message, archive_data, caption)
    await status_message.delete()


def register_emoji_handlers(dp: Dispatcher):
    emoji_filter = F.entities.func(lambda entities: any(
        entity.type == "custom_emoji" for entity in entities
    ))
    dp.message.register(handle_emoji, emoji_filter)
