import logging
import os
from typing import List, Optional, Set

from aiogram import types
from pyrogram import Client

from data.config import config
from src.utils import convert_tgs_to_json, get_file_name, send_result, create_archive, cleanup_files, Messages

logger = logging.getLogger(__name__)


async def handle_emoji_message(message: types.Message, pyro_client: Client) -> None:
    custom_emojis = _extract_emoji_ids(message)
    if not custom_emojis:
        await message.reply(Messages.NO_EMOJI)
        return

    status_message = await message.reply(Messages.LOADING)
    processed_files = []

    try:
        processed_files = await _process_emojis(custom_emojis, pyro_client)
        if processed_files:
            zip_path = await create_archive(processed_files, message.from_user.id, "emoji", message.bot)
            await send_result(message, zip_path, processed_files)
        else:
            await status_message.edit_text("❌ <b>Failed to process emoji. Please try different ones.</b>")
            return

        await status_message.delete()

    except Exception as e:
        cleanup_files(processed_files)
        await status_message.edit_text(Messages.ERROR.format(error=str(e)))


def _extract_emoji_ids(message: types.Message) -> Set[str]:
    return {
        entity.custom_emoji_id
        for entity in message.entities
        if entity.type == "custom_emoji"
    }


async def _process_emojis(emoji_ids: Set[str], pyro_client: Client) -> List[str]:
    os.makedirs(config.DOWNLOAD_DIR, exist_ok=True)
    processed_files = []
    success_count = 0
    total_count = len(emoji_ids)

    for index, emoji_id in enumerate(emoji_ids):
        try:
            files = await _process_single_emoji(emoji_id, pyro_client, index if total_count > 1 else None)
            if files:
                processed_files.extend(files)
                success_count += 1
        except Exception as e:
            logger.error(f"Error processing emoji {emoji_id}: {e}")
            continue

    return processed_files


async def _process_single_emoji(emoji_id: str,
                                pyro_client: Client,
                                index: Optional[int] = None) -> Optional[List[str]]:
    try:
        sticker_set = await pyro_client.get_custom_emoji_stickers([int(emoji_id)])
        if not sticker_set:
            logger.warning(f"No sticker found for emoji {emoji_id}")
            return None

        emoji = sticker_set[0]
        base_path = os.path.join(config.DOWNLOAD_DIR, "emoji")

        tgs_path = get_file_name(base_path, "tgs", emoji_id)
        await pyro_client.download_media(message=emoji.file_id, file_name=tgs_path)

        json_path = get_file_name(base_path, "json", emoji_id)
        if await convert_tgs_to_json(tgs_path):
            return [tgs_path, json_path]
        return [tgs_path]

    except Exception as e:
        logger.error(f"Failed to process emoji {emoji_id}: {e}")
        return None
