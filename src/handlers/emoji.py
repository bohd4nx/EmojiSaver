import json
import logging
import os
from typing import List, Optional, Set, Tuple, Dict

from aiogram import types
from pyrogram import Client

from data.config import config
from src.utils import convert_tgs_to_json, get_file_name, send_result, create_archive, cleanup_files, Messages
from src.utils.db import db

logger = logging.getLogger(__name__)


async def handle_emoji_message(message: types.Message, pyro_client: Client) -> None:
    custom_emojis = _extract_emoji_ids(message)
    if not custom_emojis:
        await message.reply(Messages.NO_EMOJI)
        return

    status_message = await message.reply(Messages.LOADING)
    processed_files = []
    animations_data = []

    try:
        processed_files = await _process_emojis(custom_emojis, pyro_client, animations_data)

        if processed_files:
            if animations_data:
                await db.save_animations(
                    user_id=message.from_user.id,
                    message_id=message.message_id,
                    animations=animations_data
                )

            zip_path = await create_archive(processed_files, message.from_user.id, message.bot)
            await send_result(message, zip_path, processed_files)
            await status_message.delete()
        else:
            await status_message.edit_text(Messages.PROCESSING_FAILED)
    except Exception as e:
        cleanup_files(processed_files)
        await status_message.edit_text(Messages.ERROR.format(error=str(e)))


def _extract_emoji_ids(message: types.Message) -> Set[str]:
    return {
        entity.custom_emoji_id
        for entity in message.entities
        if entity.type == "custom_emoji"
    }


async def _process_emojis(emoji_ids: Set[str], pyro_client: Client, animations_data: list) -> List[str]:
    os.makedirs(config.DOWNLOAD_DIR, exist_ok=True)
    processed_files = []

    for emoji_id in emoji_ids:
        try:
            files, animation = await _process_single_emoji(emoji_id, pyro_client)
            if files and animation:
                processed_files.extend(files)
                animations_data.append({
                    'emoji_id': emoji_id,
                    'animation': animation
                })
        except Exception as e:
            logger.error(f"Error processing emoji {emoji_id}: {e}")

    return processed_files


async def _process_single_emoji(emoji_id: str, pyro_client: Client) -> Tuple[Optional[List[str]], Optional[Dict]]:
    try:
        sticker_set = await pyro_client.get_custom_emoji_stickers([int(emoji_id)])
        if not sticker_set:
            logger.warning(f"No sticker found for emoji {emoji_id}")
            return None, None

        emoji = sticker_set[0]
        base_path = os.path.join(config.DOWNLOAD_DIR, "emoji")

        tgs_path = get_file_name(base_path, "tgs", emoji_id)
        await pyro_client.download_media(message=emoji.file_id, file_name=tgs_path)

        if json_path := await convert_tgs_to_json(tgs_path):
            with open(json_path, 'r', encoding='utf-8') as f:
                animation_data = json.load(f)
            return [tgs_path, json_path], animation_data

        return [tgs_path], None
    except Exception as e:
        logger.error(f"Failed to process emoji {emoji_id}: {e}")
        return None, None
