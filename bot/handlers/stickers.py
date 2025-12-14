from aiogram import Router, F
from aiogram.types import Message
from aiogram_i18n import I18nContext

from bot.core import logger
from bot.database import SessionLocal
from bot.database.crud import UserCRUD
from bot.services import download_and_convert, pack_zip, send_result

router = Router(name=__name__)


@router.message(F.sticker)
async def handle_sticker(message: Message, i18n: I18nContext) -> None:
    logger.debug(f"Received sticker: animated={message.sticker.is_animated if message.sticker else False}")

    if not message.sticker or not message.sticker.is_animated:
        logger.debug("Sticker is not animated or missing")
        await message.reply(i18n.get("no-animated-sticker"))
        return

    logger.debug(f"Processing animated sticker: {message.sticker.file_id} from user {message.from_user.id}")
    status_message = await message.reply(i18n.get("processing"))

    try:
        files, is_unsupported = await download_and_convert(
            message.sticker.file_id, message.bot
        )

        if not files:
            logger.warning("No files generated from sticker")
            await status_message.edit_text(i18n.get("processing-failed"))
            return

        archive = await pack_zip(files)
        caption = i18n.get("format-warning") if is_unsupported else None

        await send_result(message, archive, caption)
        await status_message.delete()

        async with SessionLocal() as session:
            await UserCRUD.increment_downloads(session, message.from_user.id)

    except Exception as e:
        logger.exception(f"Error handling sticker: {e}")
        await status_message.edit_text(i18n.get("processing-error", error=str(e)))
