import logging
from typing import Dict, Optional

from aiogram import types
from app.utils import (
    convert_tgs_to_json,
    send_result,
    create_archive,
    MESSAGES
)

logger = logging.getLogger(__name__)


async def handle_sticker_message(message: types.Message) -> None:
    if not message.sticker or not message.sticker.is_animated:
        await message.reply(MESSAGES["no_animated_sticker"])
        return

    status_message = await message.reply(MESSAGES["loading"])

    try:
        files_data = await _process_sticker(message.sticker.file_id, message.bot)

        if not files_data:
            await status_message.edit_text(MESSAGES["processing_failed"])
            return

        has_json = any(filename.endswith('.json') for filename in files_data)
        archive_data = await create_archive(files_data)
        await send_result(message, archive_data, has_json)
        await status_message.delete()
    except Exception as e:
        await status_message.edit_text(MESSAGES["error"].format(error=str(e)))


async def _process_sticker(file_id: str, bot) -> Dict[str, bytes]:
    try:
        tgs_data = await _download_sticker(file_id, bot)
        if not tgs_data:
            return {}

        files_data = {f"sticker_{file_id[:8]}.tgs": tgs_data}

        json_data = await convert_tgs_to_json(tgs_data)
        if json_data:
            files_data[f"sticker_{file_id[:8]}.json"] = json_data

        return files_data
    except Exception as e:
        logger.error(f"Failed to process sticker {file_id}: {e}")
        return {}


async def _download_sticker(file_id: str, bot) -> Optional[bytes]:
    try:
        file_info = await bot.get_file(file_id)
        tgs_file = await bot.download_file(file_info.file_path)
        return tgs_file.read()
    except Exception as e:
        logger.error(f"Download error: {e}")
        return None
