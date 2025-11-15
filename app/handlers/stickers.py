from aiogram import Dispatcher, F, types

from app.core import logger
from app.utils import download_and_convert, send_result, pack_zip


async def handle_sticker(message: types.Message, i18n):
    logger.debug(f"Received sticker: animated={message.sticker.is_animated if message.sticker else False}")

    if not message.sticker or not message.sticker.is_animated:
        logger.warning(f"Sticker {message.sticker.file_id if message.sticker else 'None'} is not animated or missing")
        await message.reply(i18n.get("no-animated-sticker"))
        return

    logger.debug(f"Processing animated sticker: {message.sticker.file_id}")
    status_message = await message.reply(i18n.get("loading"))

    try:
        files, is_unsupported = await download_and_convert(message.sticker.file_id, message.bot)

        if not files:
            logger.warning(f"No files generated from sticker {message.sticker.file_id}")
            await status_message.edit_text(i18n.get("processing-failed"))
            return

        logger.debug(f"Packing {len(files)} files into archive")
        archive = await pack_zip(files)
        logger.debug(f"Archive created: {len(archive)} bytes")

        caption = i18n.get("format-warning") if is_unsupported else None
        await send_result(message, archive, caption)
        await status_message.delete()
    except Exception as e:
        logger.exception(f"Error handling sticker {message.sticker.file_id if message.sticker else 'None'}: {e}")
        await status_message.edit_text(i18n.get("error", error=str(e)))


def register_sticker_handlers(dp: Dispatcher):
    dp.message.register(handle_sticker, F.sticker)
