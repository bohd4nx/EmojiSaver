import io
import logging
from typing import Dict

from aiogram import types
from pyrogram import Client
from src.utils import (
    convert_tgs_to_json,
    send_result,
    create_archive,
    MESSAGES
)

logger = logging.getLogger(__name__)


async def handle_sticker_message(message: types.Message, pyro_client: Client) -> None:
    has_valid_sticker = message.sticker and message.sticker.is_animated

    if not has_valid_sticker:
        await message.reply(MESSAGES["no_animated_sticker"])
        return

    status_message = await message.reply(MESSAGES["loading"])

    try:
        files_data = await _process_sticker(message.sticker.file_id, pyro_client)

        if files_data:
            has_json = any(filename.endswith('.json') for filename in files_data.keys())
            archive_data = await create_archive(files_data, message.bot)
            await send_result(message, archive_data, has_json)
            await status_message.delete()
        else:
            await status_message.edit_text(MESSAGES["processing_failed"])
    except Exception as e:
        await status_message.edit_text(MESSAGES["error"].format(error=str(e)))


async def _process_sticker(file_id: str, pyro_client: Client) -> Dict[str, bytes]:
    try:
        tgs_buffer = io.BytesIO()
        await pyro_client.download_media(message=file_id, file=tgs_buffer)
        tgs_data = tgs_buffer.getvalue()

        files_data = {f"sticker_{file_id[:8]}.tgs": tgs_data}

        json_data = await convert_tgs_to_json(tgs_data)
        if json_data:
            files_data[f"sticker_{file_id[:8]}.json"] = json_data

        return files_data
    except Exception as e:
        logger.error(f"Failed to process sticker {file_id}: {e}")
        return {}
