from urllib.parse import urlparse

from aiogram import Router, F
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import Message, Sticker
from aiogram_i18n import I18nContext

from bot.core import logger
from bot.database import SessionLocal
from bot.database.crud import DownloadsCRUD
from bot.services import download_and_convert, pack_zip, send_result

router = Router(name=__name__)


@router.message(F.text.regexp(r"https://t\.me/(addstickers|addemoji)/\w+"))
async def handle_pack(message: Message, i18n: I18nContext) -> None:
    url = message.text.strip()
    logger.debug(f"Received pack URL: {url} from user {message.from_user.id}")

    parsed = urlparse(url)
    path_parts = parsed.path.split('/')

    if len(path_parts) < 3:
        logger.warning(f"Invalid pack URL: {url}")
        await message.reply(i18n.get("invalid-input"))
        return

    pack_type, pack_name = path_parts[1], path_parts[2]
    logger.debug(f"Processing pack: type={pack_type}, name={pack_name}")

    status_message = await message.reply(i18n.get("processing-pack", current=0, total=0))

    try:
        result = await get_pack_items(message, pack_name)
        if not result:
            logger.warning(f"Pack not found: {pack_name}")
            await status_message.edit_text(i18n.get("pack-not-found"))
            return

        items, pack_title = result

        if not items:
            logger.warning(f"Empty pack: {pack_name}")
            await status_message.edit_text(i18n.get("processing-failed"))
            return

        files, has_unsupported = await process_items(items, message.bot, status_message, i18n)

        if not files:
            logger.warning("No files generated from pack")
            await status_message.edit_text(i18n.get("processing-failed"))
            return

        archive = await pack_zip(files)
        await send_result(message, archive, i18n, has_unsupported, pack_title)
        await status_message.delete()
        logger.debug(f"Pack processed successfully: {pack_title}")

        async with SessionLocal() as session:
            await DownloadsCRUD.add_download(session, message.from_user.id, "pack", pack_name)

    except Exception as e:
        logger.exception(f"Error handling pack: {e}")
        await status_message.edit_text(i18n.get("processing-error", error=str(e)))


async def get_pack_items(
        message: Message, pack_name: str
) -> tuple[list[Sticker], str] | None:
    try:
        # logger.debug(f"Fetching pack: type={pack_type}, name={pack_name}")
        sticker_set = await message.bot.get_sticker_set(pack_name)
        logger.debug(f"Found pack: {sticker_set.title}, items={len(sticker_set.stickers)}")
        return sticker_set.stickers, sticker_set.title
    except TelegramBadRequest as e:
        if "STICKERSET_INVALID" in str(e):
            logger.warning(f"Invalid sticker set: {pack_name}")
        else:
            logger.error(f"Telegram error fetching pack {pack_name}: {e}")
        return None


async def process_items(
        items: list[Sticker],
        bot,
        status_message: Message,
        i18n: I18nContext
) -> tuple[dict, bool]:
    files = {}
    has_unsupported = False
    total = len(items)

    update_interval = 50 if total > 500 else 20 if total > 100 else 10
    logger.debug(f"Processing {total} items with update interval {update_interval}")

    for idx, item in enumerate(items, 1):
        if idx % update_interval == 0 or idx == total:
            try:
                await status_message.edit_text(
                    i18n.get("processing-pack", current=idx, total=total)
                )
            except TelegramBadRequest as e:
                logger.warning(f"Failed to update status: {e}")
            except Exception as e:
                logger.error(f"Unexpected error updating status: {e}")

        try:
            item_files, is_unsupported = await download_and_convert(item.file_id, bot)
            files.update(item_files)
            has_unsupported = has_unsupported or is_unsupported
        except Exception as e:
            logger.error(f"Failed to process item {idx}: {e}")

    logger.debug(f"Processed {total} items: {len(files)} files, has_unsupported={has_unsupported}")
    return files, has_unsupported
