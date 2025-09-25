import io
import logging
import zipfile
from typing import Dict

from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder

logger = logging.getLogger(__name__)


async def pack_zip(files: Dict[str, bytes]) -> bytes:
    try:
        buffer = io.BytesIO()

        with zipfile.ZipFile(buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
            for name, data in files.items():
                if len(files) > 2:
                    file_id = name.split('.')[0]
                    zip_file.writestr(f"[{file_id}]/{name}", data)
                else:
                    zip_file.writestr(name, data)

        buffer.seek(0)
        return buffer.getvalue()
    except Exception as e:
        logger.error(f"Failed to create archive: {e}")
        raise


async def send_result(message: types.Message, data: bytes) -> None:
    try:
        builder = InlineKeyboardBuilder()
        filename = f"@{(await message.bot.me()).username}.zip"

        await message.reply_document(
            document=types.BufferedInputFile(data, filename=filename),
            reply_markup=builder.as_markup()
        )
    except Exception as e:
        logger.error(f"Failed to send result: {e}")
        raise
