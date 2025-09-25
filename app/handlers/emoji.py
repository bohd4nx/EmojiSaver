import logging
from typing import Dict, Set

from aiogram import types

from app.utils import tgs_to_json, tgs_to_lottie, send_result, pack_zip, MESSAGES

logger = logging.getLogger(__name__)


async def handle_emoji(message: types.Message) -> None:
    emoji_ids = {entity.custom_emoji_id for entity in message.entities
                 if entity.type == "custom_emoji"}

    if not emoji_ids:
        await message.reply(MESSAGES["no_emoji"])
        return

    status_message = await message.reply(MESSAGES["loading"])

    try:
        files = await process_all_emojis(emoji_ids, message.bot)
        await handle_result(message, status_message, files)
    except Exception as e:
        await status_message.edit_text(MESSAGES["error"].format(error=str(e)))


async def process_all_emojis(emoji_ids: Set[str], bot) -> Dict[str, bytes]:
    files = {}
    for emoji_id in emoji_ids:
        try:
            emoji_files = await process_emoji(emoji_id, bot)
            files.update(emoji_files)
        except Exception as e:
            logger.error(f"Error processing emoji {emoji_id}: {e}")
    return files


async def process_emoji(emoji_id: str, bot) -> Dict[str, bytes]:
    try:
        stickers = await bot.get_custom_emoji_stickers([emoji_id])
        if not stickers:
            return {}

        emoji = stickers[0]
        file_info = await bot.get_file(emoji.file_id)
        tgs_file = await bot.download_file(file_info.file_path)

        if not tgs_file:
            return {}

        tgs_data = tgs_file.read()

        return {
            f"{emoji_id}.tgs": tgs_data,
            f"{emoji_id}.json": await tgs_to_json(tgs_data) or b"",
            f"{emoji_id}.lottie": await tgs_to_lottie(tgs_data) or b""
        }
    except Exception as e:
        logger.error(f"Failed to process emoji {emoji_id}: {e}")
        return {}


async def handle_result(message: types.Message, status_message: types.Message,
                        files: Dict[str, bytes]) -> None:
    if not files:
        await status_message.edit_text(MESSAGES["processing_failed"])
        return

    archive_data = await pack_zip(files)
    await send_result(message, archive_data)
    await status_message.delete()
