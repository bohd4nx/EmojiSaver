from typing import Dict, Set

from aiogram import Router, F, Bot
from aiogram.types import Message
from aiogram_i18n import I18nContext

from bot.core import logger
from bot.services import download_and_convert, pack_zip, send_result

router = Router(name=__name__)


@router.message(F.entities.func(lambda entities: any(entity.type == "custom_emoji" for entity in entities)))
async def handle_emoji(message: Message, i18n: I18nContext) -> None:
    emoji_ids = {entity.custom_emoji_id for entity in message.entities if entity.type == "custom_emoji"}
    logger.debug(f"Detected {len(emoji_ids)} custom emoji in message from user {message.from_user.id}")

    if not emoji_ids:
        logger.debug("No custom emoji found in message")
        await message.reply(i18n.get("no-custom-emoji"))
        return

    status_message = await message.reply(i18n.get("processing"))
    logger.debug(f"Started processing emoji batch: {emoji_ids}")

    try:
        files, has_unsupported = await process_all_emojis(emoji_ids, message.bot)

        if not files:
            logger.warning("No files generated from emoji processing")
            await status_message.edit_text(i18n.get("processing-failed"))
            return

        archive_data = await pack_zip(files)
        caption = i18n.get("format-warning") if has_unsupported else None

        await send_result(message, archive_data, caption)
        await status_message.delete()
    except Exception as e:
        logger.exception(f"Error handling emoji: {e}")
        await status_message.edit_text(i18n.get("processing-error", error=str(e)))


async def process_all_emojis(emoji_ids: Set[str], bot: Bot) -> tuple[Dict[str, bytes], bool]:
    files = {}
    has_unsupported = False

    for emoji_id in emoji_ids:
        logger.debug(f"Processing emoji: {emoji_id}")
        try:
            emoji_files, is_unsupported = await process_emoji(emoji_id, bot)
            files.update(emoji_files)
            has_unsupported = has_unsupported or is_unsupported
        except Exception as e:
            logger.error(f"Failed to process emoji {emoji_id}: {e}")

    return files, has_unsupported


async def process_emoji(emoji_id: str, bot: Bot) -> tuple[Dict[str, bytes], bool]:
    try:
        stickers = await bot.get_custom_emoji_stickers([emoji_id])

        if not stickers:
            logger.warning(f"No stickers found for emoji: {emoji_id}")
            return {}, False

        return await download_and_convert(stickers[0].file_id, bot)

    except Exception as e:
        logger.exception(f"Failed to process emoji {emoji_id}: {e}")
        return {}, False
