import io
import zipfile
from typing import Dict, Optional

from aiogram.types import Message, BufferedInputFile

from bot.core import logger


async def pack_zip(files: Dict[str, bytes]) -> bytes:
    try:
        logger.debug(f"Packing ZIP archive: {len(files)} files")
        buffer = io.BytesIO()

        with zipfile.ZipFile(buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
            for name, data in files.items():
                if len(files) > 2:
                    file_id = name.split('.')[0]
                    zip_file.writestr(f"{file_id}/{name}", data)
                else:
                    zip_file.writestr(name, data)
                
                logger.debug(f"Added to archive: {len(data)} bytes")

        buffer.seek(0)
        result = buffer.getvalue()
        logger.debug(f"ZIP archive created: {len(result)} bytes")
        return result
    except Exception as e:
        logger.error(f"Failed to create archive: {e}")
        raise


async def send_result(message: Message, data: bytes, caption: Optional[str] = None, filename: Optional[str] = None) -> None:
    try:
        bot_info = await message.bot.me()
        
        if filename:
            filename = f"{filename} by @{bot_info.username}.zip"
        else:
            filename = f"@{bot_info.username}.zip"
        
        logger.debug(f"Sending result: filename={filename}, size={len(data)} bytes")

        await message.reply_document(
            document=BufferedInputFile(data, filename=filename),
            caption=caption
        )
        logger.debug(f"Result sent successfully to user: {message.from_user.id}")
    except Exception as e:
        logger.error(f"Failed to send result: {e}")
        raise
