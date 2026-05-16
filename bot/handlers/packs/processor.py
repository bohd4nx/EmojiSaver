from contextlib import suppress

from aiogram import Bot
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import Message, Sticker
from aiogram_i18n import I18nContext

from bot.core import logger
from bot.services import download_and_convert


async def get_pack_items(message: Message, pack_name: str) -> tuple[list[Sticker], str] | None:
    try:
        assert message.bot
        sticker_set = await message.bot.get_sticker_set(pack_name)
        return sticker_set.stickers, sticker_set.title
    except TelegramBadRequest as exc:
        if "STICKERSET_INVALID" in str(exc):
            logger.warning("Pack not found: %s", pack_name)
        else:
            logger.error("Telegram error fetching pack %s: %s", pack_name, exc)
        return None


async def process_items(
    items: list[Sticker],
    bot: Bot,
    status_msg: Message,
    i18n: I18nContext,
) -> tuple[dict[str, bytes], bool]:
    files: dict[str, bytes] = {}
    has_unsupported = False
    total = len(items)
    # throttle status message edits to avoid hitting Telegram rate limits:
    # large packs get less frequent updates to reduce API calls.
    update_interval = 75 if total > 500 else 25 if total > 100 else 15

    for idx, item in enumerate(items, 1):
        if idx % update_interval == 0 or idx == total:
            with suppress(TelegramBadRequest):
                await status_msg.edit_text(i18n.get("processing-pack", current=idx, total=total))

        try:
            item_files, is_unsupported = await download_and_convert(item.file_id, bot)
            files |= item_files
            has_unsupported = has_unsupported or is_unsupported
        except Exception as exc:
            logger.error("Failed to process item %s: %s", idx, exc)

    return files, has_unsupported
