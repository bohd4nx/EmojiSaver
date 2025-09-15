import io
import logging
import zipfile
from typing import Dict

from aiogram import types, Bot
from aiogram.utils.keyboard import InlineKeyboardBuilder

from .texts import MESSAGES

logger = logging.getLogger(__name__)


async def create_archive(files_data: Dict[str, bytes], bot: Bot) -> bytes:
    try:
        archive_buffer = io.BytesIO()
        bot_username = (await bot.me()).username

        with zipfile.ZipFile(archive_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
            for filename, file_data in files_data.items():
                if len(files_data) > 2:
                    file_id = filename.split('.')[0]
                    zip_file.writestr(f"[{file_id}]/{filename}", file_data)
                else:
                    zip_file.writestr(filename, file_data)

        archive_buffer.seek(0)
        return archive_buffer.getvalue()
    except Exception as e:
        logger.error(f"Failed to create archive: {e}")
        raise


async def send_result(message: types.Message, archive_data: bytes, has_json_conversion: bool) -> None:
    try:
        builder = InlineKeyboardBuilder()
        caption = None if has_json_conversion else MESSAGES["success_tgs_only"]

        filename = f"@{(await message.bot.me()).username}.zip"

        await message.reply_document(
            document=types.BufferedInputFile(archive_data, filename=filename),
            caption=caption,
            reply_markup=builder.as_markup()
        )
    except Exception as e:
        logger.error(f"Failed to send result: {e}")
        raise
