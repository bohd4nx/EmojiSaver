import json

from aiogram import Bot, F, Router
from aiogram.types import Message
from aiogram_i18n import I18nContext

from bot.__meta__ import DEVELOPER_URL
from bot.core import logger
from bot.database import SessionLocal
from bot.database.crud import add_download, get_or_create_user
from bot.services import download_and_convert, pack_zip, send_result
from bot.utils import status_message

router = Router(name=__name__)


@router.message(F.entities.func(lambda entities: any(e.type == "custom_emoji" for e in entities)))
async def handle_emoji(message: Message, i18n: I18nContext) -> None:
    emoji_ids = {e.custom_emoji_id for e in message.entities if e.type == "custom_emoji"}

    if not emoji_ids:
        logger.debug(f"No custom emoji found in message from user {message.from_user.id}")
        await message.reply(i18n.get("no-custom-emoji"))
        return

    try:
        async with status_message(message, i18n) as status_msg:
            files, has_unsupported = await process_all_emojis(emoji_ids, message.bot)

            if not files:
                logger.warning(f"No files generated from emoji {json.dumps(list(emoji_ids))}")
                await status_msg.edit_text(i18n.get("processing-failed", developer=DEVELOPER_URL))
                return

            await send_result(message, await pack_zip(files), i18n, has_unsupported)

        async with SessionLocal() as session:
            user = message.from_user
            await get_or_create_user(session, user.id, user.username, user.first_name)
            await add_download(session, user.id, "emoji", json.dumps(list(emoji_ids)))

    except Exception as e:
        logger.exception(f"Error handling emoji: {e}")
        await message.reply(i18n.get("processing-error", error=str(e), developer=DEVELOPER_URL))


async def process_all_emojis(emoji_ids: set[str], bot: Bot) -> tuple[dict[str, bytes], bool]:
    files: dict[str, bytes] = {}
    has_unsupported = False

    for emoji_id in emoji_ids:
        try:
            emoji_files, is_unsupported = await process_emoji(emoji_id, bot)
            files |= emoji_files
            has_unsupported = has_unsupported or is_unsupported
        except Exception as e:
            logger.error(f"Failed to process emoji {emoji_id}: {e}")

    return files, has_unsupported


async def process_emoji(emoji_id: str, bot: Bot) -> tuple[dict[str, bytes], bool]:
    try:
        stickers = await bot.get_custom_emoji_stickers([emoji_id])
        if not stickers:
            logger.warning(f"No stickers found for emoji: {emoji_id}")
            return {}, False
        return await download_and_convert(stickers[0].file_id, bot)
    except Exception as e:
        logger.exception(f"Failed to process emoji {emoji_id}: {e}")
        return {}, False
