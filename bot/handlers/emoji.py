import json

from aiogram import Bot, F, Router
from aiogram.types import Message
from aiogram_i18n import I18nContext
from sqlalchemy.ext.asyncio import AsyncSession

from bot.core import logger
from bot.database.crud import add_download, get_or_create_user
from bot.services import download_and_convert, pack_zip, send_result
from bot.utils import status_message

router = Router(name=__name__)


@router.message(
    F.entities.func(lambda entities: any(e.type == "custom_emoji" for e in entities))
)
async def handle_emoji(
    message: Message, i18n: I18nContext, session: AsyncSession
) -> None:
    emoji_ids = {
        e.custom_emoji_id for e in message.entities if e.type == "custom_emoji"
    }

    if not emoji_ids:
        logger.debug(
            "No custom emoji found in message from user %s", message.from_user.id
        )
        await message.reply(i18n.get("no-custom-emoji"))
        return

    async with status_message(message, i18n) as status_msg:
        files, has_unsupported = await process_all_emojis(emoji_ids, message.bot)

        if not files:
            logger.warning(
                "No files generated from emoji %s", json.dumps(list(emoji_ids))
            )
            await status_msg.edit_text(i18n.get("processing-failed"))
            return

        await send_result(message, await pack_zip(files), i18n, has_unsupported)

    user = message.from_user
    await get_or_create_user(session, user.id, user.username, user.first_name)
    await add_download(session, user.id, "emoji", json.dumps(list(emoji_ids)))


async def process_all_emojis(
    emoji_ids: set[str], bot: Bot
) -> tuple[dict[str, bytes], bool]:
    files: dict[str, bytes] = {}
    has_unsupported = False

    for emoji_id in emoji_ids:
        try:
            emoji_files, is_unsupported = await process_emoji(emoji_id, bot)
            files |= emoji_files
            has_unsupported = has_unsupported or is_unsupported
        except Exception as exc:
            logger.error("Failed to process emoji %s: %s", emoji_id, exc)

    return files, has_unsupported


async def process_emoji(emoji_id: str, bot: Bot) -> tuple[dict[str, bytes], bool]:
    try:
        stickers = await bot.get_custom_emoji_stickers([emoji_id])
        if not stickers:
            logger.warning("No stickers found for emoji: %s", emoji_id)
            return {}, False
        return await download_and_convert(stickers[0].file_id, bot)
    except Exception:
        logger.exception("Failed to process emoji %s", emoji_id)
        return {}, False
