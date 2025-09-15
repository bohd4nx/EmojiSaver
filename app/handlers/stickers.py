import logging
from typing import Dict, Optional

from aiogram import types
from app.utils import (
    convert_tgs_to_json,
    send_result,
    create_archive,
    MESSAGES
)
from pyrogram import Client
from pyrogram.errors import FileReferenceExpired, RPCError

logger = logging.getLogger(__name__)


# TODO: handle Telegram says: [400 FILE_REFERENCE_EXPIRED] and refactore code

async def handle_sticker_message(message: types.Message, pyro_client: Client) -> None:
    if not message.sticker or not message.sticker.is_animated:
        await message.reply(MESSAGES["no_animated_sticker"])
        return

    status_message = await message.reply(MESSAGES["loading"])

    try:
        files_data = await _process_sticker(message.sticker.file_id, pyro_client)

        if not files_data:
            await status_message.edit_text(MESSAGES["processing_failed"])
            return

        has_json = any(filename.endswith('.json') for filename in files_data)
        archive_data = await create_archive(files_data)
        await send_result(message, archive_data, has_json)
        await status_message.delete()
    except Exception as e:
        await status_message.edit_text(MESSAGES["error"].format(error=str(e)))


async def _process_sticker(file_id: str, pyro_client: Client) -> Dict[str, bytes]:
    try:
        tgs_data = await _download_sticker(file_id, pyro_client)
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


async def _download_sticker(file_id: str, pyro_client: Client) -> Optional[bytes]:
    try:
        tgs_buffer = await pyro_client.download_media(message=file_id, in_memory=True)

        if hasattr(tgs_buffer, 'getvalue'):
            return tgs_buffer.getvalue()
        elif isinstance(tgs_buffer, bytes):
            return tgs_buffer

        logger.error(f"Unexpected download result type: {type(tgs_buffer)}")
        return None
    except FileReferenceExpired:
        logger.error(f"File reference expired for sticker {file_id}")
        return None
    except RPCError as e:
        logger.error(f"Telegram API error: {e}")
        return None
