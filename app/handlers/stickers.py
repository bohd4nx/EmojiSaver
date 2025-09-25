import logging
from typing import Dict, Optional

from aiogram import types

from app.utils import (
    tgs_to_json,
    tgs_to_lottie,
    send_result,
    pack_zip,
    MESSAGES
)

logger = logging.getLogger(__name__)


async def handle_sticker(message: types.Message) -> None:
    if not message.sticker or not message.sticker.is_animated:
        await message.reply(MESSAGES["no_animated_sticker"])
        return

    status_message = await message.reply(MESSAGES["loading"])

    try:
        files = await process_sticker(message.sticker.file_id, message.bot)

        if not files:
            await status_message.edit_text(MESSAGES["processing_failed"])
            return

        archive = await pack_zip(files)
        await send_result(message, archive)
        await status_message.delete()
    except Exception as e:
        await status_message.edit_text(MESSAGES["error"].format(error=str(e)))


async def process_sticker(file_id: str, bot) -> Dict[str, bytes]:
    try:
        tgs_data = await download_sticker(file_id, bot)
        if not tgs_data:
            return {}

        return {
            f"{file_id}.tgs": tgs_data,
            f"{file_id}.json": await tgs_to_json(tgs_data) or b"",
            f"{file_id}.lottie": await tgs_to_lottie(tgs_data) or b""
        }
    except Exception as e:
        logger.error(f"Failed to process sticker {file_id}: {e}")
        return {}


async def download_sticker(file_id: str, bot) -> Optional[bytes]:
    try:
        file_info = await bot.get_file(file_id)
        file = await bot.download_file(file_info.file_path)
        return file.read()
    except Exception as e:
        logger.error(f"Download error: {e}")
        return None
