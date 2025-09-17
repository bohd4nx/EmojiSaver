import logging
from typing import Dict, Set

from aiogram import types
from app.utils import convert_tgs_to_json, send_result, create_archive, MESSAGES

logger = logging.getLogger(__name__)


async def handle_emoji_message(message: types.Message) -> None:
    custom_emojis = _extract_emoji_ids(message)

    if not custom_emojis:
        await message.reply(MESSAGES["no_emoji"])
        return

    status_message = await message.reply(MESSAGES["loading"])

    try:
        files_data = await _process_emojis(custom_emojis, message.bot)
        await _handle_processing_result(message, status_message, files_data)
    except Exception as e:
        await status_message.edit_text(MESSAGES["error"].format(error=str(e)))


def _extract_emoji_ids(message: types.Message) -> Set[str]:
    return {
        entity.custom_emoji_id
        for entity in message.entities
        if entity.type == "custom_emoji"
    }


async def _handle_processing_result(message: types.Message, status_message: types.Message,
                                    files_data: Dict[str, bytes]) -> None:
    if not files_data:
        await status_message.edit_text(MESSAGES["processing_failed"])
        return

    has_json = any(filename.endswith('.json') for filename in files_data)
    archive_data = await create_archive(files_data)
    await send_result(message, archive_data, has_json)
    await status_message.delete()


async def _process_emojis(emoji_ids: Set[str], bot) -> Dict[str, bytes]:
    files_data = {}

    for emoji_id in emoji_ids:
        try:
            emoji_files = await _process_single_emoji(emoji_id, bot)
            files_data.update(emoji_files)
        except Exception as e:
            logger.error(f"Error processing emoji {emoji_id}: {e}")

    return files_data


async def _process_single_emoji(emoji_id: str, bot) -> Dict[str, bytes]:
    try:
        stickers = await bot.get_custom_emoji_stickers([emoji_id])

        if not stickers:
            logger.warning(f"No sticker found for emoji {emoji_id}")
            return {}

        emoji = stickers[0]

        file_info = await bot.get_file(emoji.file_id)
        tgs_file = await bot.download_file(file_info.file_path)

        if not tgs_file:
            logger.error(f"Empty data received for emoji {emoji_id}")
            return {}

        tgs_data = tgs_file.read()
        files_data = {f"{emoji_id}.tgs": tgs_data}

        json_data = await convert_tgs_to_json(tgs_data)
        if json_data:
            files_data[f"{emoji_id}.json"] = json_data

        return files_data

    except Exception as e:
        logger.error(f"Failed to process emoji {emoji_id}: {e}")
        return {}
