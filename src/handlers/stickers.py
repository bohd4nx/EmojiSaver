import json
import os
from typing import Optional, List

from aiogram import types
from pyrogram import Client

from data.config import config
from src.utils import convert_tgs_to_json, get_file_name, send_result, create_archive, cleanup_files, Messages
from src.utils.db import db


async def handle_sticker_message(message: types.Message, pyro_client: Client) -> None:
    if not message.sticker or not message.sticker.is_animated:
        await message.reply(Messages.NO_ANIMATED_STICKER)
        return

    status_message = await message.reply(Messages.LOADING)
    processed_files = []
    animations_data = []

    try:
        processed_files = await _process_sticker(message.sticker.file_id, pyro_client, message.from_user.id,
                                                 animations_data
                                                 )
        if processed_files:
            if animations_data:
                await db.save_animations(
                    user_id=message.from_user.id,
                    message_id=message.message_id,
                    animations=animations_data
                )
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


async def _process_sticker(file_id: str, pyro_client: Client, user_id: int, animations_data: list) -> Optional[
    List[str]]:
    os.makedirs(config.DOWNLOAD_DIR, exist_ok=True)
    base_path = os.path.join(config.DOWNLOAD_DIR, "sticker")

    tgs_path = get_file_name(base_path, "tgs", file_id)
    await pyro_client.download_media(message=file_id, file_name=tgs_path)

    json_path = get_file_name(base_path, "json", file_id)
    if json_path := await convert_tgs_to_json(tgs_path):
        with open(json_path, 'r', encoding='utf-8') as f:
            animation_data = json.load(f)
        animations_data.append({
            'sticker_id': file_id,
            'animation': animation_data
        })
        return [tgs_path, json_path]
    return [tgs_path]
