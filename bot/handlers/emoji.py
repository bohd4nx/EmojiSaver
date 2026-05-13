import json

from aiogram import Bot, F, Router
from aiogram.types import Message
from aiogram_i18n import I18nContext
from sqlalchemy.ext.asyncio import AsyncSession

from bot.core import logger
from bot.database.crud import add_download, get_or_create_user
from bot.handlers.status import status_message
from bot.services import download_and_convert, pack_zip, send_result

router = Router(name=__name__)


# match any message that contains at least one custom emoji entity
@router.message(F.entities.func(lambda entities: any(e.type == "custom_emoji" for e in entities)))
async def handle_emoji(message: Message, i18n: I18nContext, session: AsyncSession) -> None:
    entities = message.entities or []
    emoji_ids: set[str] = {e.custom_emoji_id for e in entities if e.type == "custom_emoji" and e.custom_emoji_id is not None}

    if not emoji_ids:
        logger.debug(
            "No custom emoji found in message from user %s",
            message.from_user.id if message.from_user else "unknown",
        )
        await message.reply(i18n.get("no-custom-emoji"))
        return

    assert message.bot
    async with status_message(message, i18n) as status_msg:
        files, has_unsupported = await process_all_emojis(emoji_ids, message.bot)

        if not files:
            logger.warning("No files generated from emoji %s", json.dumps(list(emoji_ids)))
            await status_msg.edit_text(i18n.get("processing-failed"))
            return

        await send_result(message, await pack_zip(files), i18n, has_unsupported)

    user = message.from_user
    if user:
        await get_or_create_user(session, user.id, user.username)
        await add_download(session, user.id, "emoji", json.dumps(list(emoji_ids)))


async def process_all_emojis(emoji_ids: set[str], bot: Bot) -> tuple[dict[str, bytes], bool]:
    files: dict[str, bytes] = {}
    has_unsupported = False

    try:
        stickers = await bot.get_custom_emoji_stickers(list(emoji_ids))
    except Exception as exc:
        logger.error("Failed to fetch custom emoji stickers: %s", exc)
        return {}, False

    for sticker in stickers:
        try:
            emoji_files, is_unsupported = await download_and_convert(sticker.file_id, bot)
            files |= emoji_files
            has_unsupported = has_unsupported or is_unsupported
        except Exception as exc:
            logger.error("Failed to process emoji %s: %s", sticker.file_id, exc)

    return files, has_unsupported
