import contextlib

from aiogram import Bot, F, Router
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import Message, Sticker
from aiogram_i18n import I18nContext

from bot.__meta__ import DEVELOPER_URL
from bot.core import logger
from bot.database import SessionLocal
from bot.database.crud import add_download, get_or_create_user
from bot.services import download_and_convert, pack_zip, send_result
from bot.utils import status_message

router = Router(name=__name__)


@router.message(F.text.regexp(r"https://t\.me/(addstickers|addemoji)/\w+"))
async def handle_pack(message: Message, i18n: I18nContext) -> None:
    pack_name = message.text.strip().rstrip("/").split("/")[-1]

    try:
        result = await get_pack_items(message, pack_name)
        if not result:
            await message.reply(i18n.get("pack-not-found"))
            return

        items, pack_title = result
        if not items:
            logger.warning(f"Empty pack: {pack_name}")
            await message.reply(i18n.get("processing-failed", developer=DEVELOPER_URL))
            return

        async with status_message(message, i18n, "processing-pack", current=0, total=len(items)) as status_msg:
            files, has_unsupported = await process_items(items, message.bot, status_msg, i18n)

            if not files:
                logger.warning(f"No files generated from pack {pack_name}")
                await status_msg.edit_text(i18n.get("processing-failed", developer=DEVELOPER_URL))
                return

            await send_result(message, await pack_zip(files), i18n, has_unsupported, pack_title)

        async with SessionLocal() as session:
            user = message.from_user
            await get_or_create_user(session, user.id, user.username, user.first_name)
            await add_download(session, user.id, "pack", pack_name)

    except Exception as e:
        logger.exception(f"Error handling pack: {e}")
        await message.reply(i18n.get("processing-error", error=str(e), developer=DEVELOPER_URL))


async def get_pack_items(message: Message, pack_name: str) -> tuple[list[Sticker], str] | None:
    try:
        sticker_set = await message.bot.get_sticker_set(pack_name)
        return sticker_set.stickers, sticker_set.title
    except TelegramBadRequest as e:
        if "STICKERSET_INVALID" in str(e):
            logger.warning(f"Pack not found: {pack_name}")
        else:
            logger.error(f"Telegram error fetching pack {pack_name}: {e}")
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
    update_interval = 75 if total > 500 else 25 if total > 100 else 15

    for idx, item in enumerate(items, 1):
        if idx % update_interval == 0 or idx == total:
            with contextlib.suppress(TelegramBadRequest):
                await status_msg.edit_text(i18n.get("processing-pack", current=idx, total=total))

        try:
            item_files, is_unsupported = await download_and_convert(item.file_id, bot)
            files |= item_files
            has_unsupported = has_unsupported or is_unsupported
        except Exception as e:
            logger.error(f"Failed to process item {idx}: {e}")

    return files, has_unsupported
