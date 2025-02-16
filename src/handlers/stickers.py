import os
from typing import Optional, List

from aiogram import types
from pyrogram import Client

from data.config import config
from src.utils import convert_tgs_to_json, get_file_name, send_result, create_archive, cleanup_files, Messages


async def handle_sticker_message(message: types.Message, pyro_client: Client) -> None:
    if not message.sticker or not message.sticker.is_animated:
        await message.reply(Messages.NO_ANIMATED_STICKER)
        return

    status_message = await message.reply(Messages.LOADING)
    processed_files = []

    try:
        processed_files = await _process_sticker(message.sticker.file_id, pyro_client)
        if processed_files:
            zip_path = await create_archive(
                processed_files,
                message.from_user.id,
                "sticker",
                message.bot
            )
            await send_result(message, zip_path, processed_files)

        await status_message.delete()

    except Exception as e:
        cleanup_files(processed_files)
        await status_message.edit_text(Messages.ERROR.format(error=str(e)))


async def _process_sticker(file_id: str, pyro_client: Client) -> Optional[List[str]]:
    os.makedirs(config.DOWNLOAD_DIR, exist_ok=True)
    base_path = os.path.join(config.DOWNLOAD_DIR, "sticker")

    tgs_path = get_file_name(base_path, "tgs")
    await pyro_client.download_media(message=file_id, file_name=tgs_path)

    json_path = get_file_name(base_path, "json")
    if await convert_tgs_to_json(tgs_path):
        return [tgs_path, json_path]
    return [tgs_path]
