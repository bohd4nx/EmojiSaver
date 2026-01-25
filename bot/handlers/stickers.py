from aiogram import Router, F
from aiogram.types import Message
from aiogram_i18n import I18nContext

from bot.core import logger
from bot.database import SessionLocal
from bot.database.crud import DownloadsCRUD, UserCRUD
from bot.services import download_and_convert, pack_zip, send_result
from bot.utils import emoji

router = Router(name=__name__)


@router.message(F.sticker)
async def handle_sticker(message: Message, i18n: I18nContext) -> None:
    if not message.sticker:
        return

    logger.debug(f"Processing sticker: {message.sticker.file_id} from user {message.from_user.id}")
    status_message = await message.reply(i18n.get("processing", processing=emoji['processing']))

    try:
        files, is_unsupported = await download_and_convert(
            message.sticker.file_id, message.bot
        )

        if not files:
            logger.warning("No files generated from sticker")
            await status_message.edit_text(i18n.get("processing-failed", forbidden=emoji['forbidden']))
            return

        archive = await pack_zip(files)
        await send_result(message, archive, i18n, is_unsupported)
        await status_message.delete()

        async with SessionLocal() as session:
            await UserCRUD.get_or_create(
                session=session,
                user_id=message.from_user.id,
                username=message.from_user.username,
                full_name=message.from_user.full_name
            )
            await DownloadsCRUD.add_download(session, message.from_user.id, "sticker", message.sticker.file_id)

    except Exception as e:
        logger.exception(f"Error handling sticker: {e}")
        await status_message.edit_text(i18n.get("processing-error", error=str(e), forbidden=emoji['forbidden']))
