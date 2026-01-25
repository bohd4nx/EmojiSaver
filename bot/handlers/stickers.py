from aiogram import Router, F
from aiogram.types import Message
from aiogram_i18n import I18nContext

from bot.__meta__ import DEVELOPER_URL
from bot.core import logger
from bot.database import SessionLocal
from bot.database.crud import DownloadsCRUD, UserCRUD
from bot.services import download_and_convert, pack_zip, send_result
from bot.utils import emoji, status_message

router = Router(name=__name__)


@router.message(F.sticker)
async def handle_sticker(message: Message, i18n: I18nContext) -> None:
    if not message.sticker:
        return

    logger.debug(f"Processing sticker: {message.sticker.file_id} from user {message.from_user.id}")

    try:
        async with status_message(message, i18n) as status_msg:
            files, is_unsupported = await download_and_convert(
                message.sticker.file_id, message.bot
            )

            if not files:
                logger.warning("No files generated from sticker")
                await status_msg.edit_text(
                    i18n.get("processing-failed", forbidden=emoji['forbidden'], telegram=emoji['telegram'],
                             developer=DEVELOPER_URL))
                return

            archive = await pack_zip(files)
            await send_result(message, archive, i18n, is_unsupported)

        async with SessionLocal() as session:
            await UserCRUD.get_or_create(
                session,
                message.from_user.id,
                message.from_user.username,
                message.from_user.full_name
            )
            await DownloadsCRUD.add_download(session, message.from_user.id, "sticker", message.sticker.file_id)

    except Exception as e:
        logger.exception(f"Error handling sticker: {e}")
        await message.reply(
            i18n.get("processing-error", error=str(e), forbidden=emoji['forbidden'], telegram=emoji['telegram'],
                     developer=DEVELOPER_URL))
