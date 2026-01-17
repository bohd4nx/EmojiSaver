import io
import zipfile

from aiogram.types import Message, BufferedInputFile
from aiogram_i18n import I18nContext

MAX_ARCHIVE_SIZE = 45 * 1024 * 1024 # 45 MB


async def pack_zip(files: dict[str, bytes]) -> list[bytes]:
    archives = []
    current_buffer = io.BytesIO()
    current_zip = zipfile.ZipFile(current_buffer, 'w', zipfile.ZIP_DEFLATED)

    for name, data in files.items():
        if len(files) > 2:
            file_id = name.split('.')[0]
            current_zip.writestr(f"{file_id}/{name}", data)
        else:
            current_zip.writestr(name, data)
        
        current_buffer.seek(0)
        current_archive_size = len(current_buffer.getvalue())
        
        if current_archive_size > MAX_ARCHIVE_SIZE:
            current_zip.close()
            current_buffer.seek(0)
            archives.append(current_buffer.getvalue())
            
            current_buffer = io.BytesIO()
            current_zip = zipfile.ZipFile(current_buffer, 'w', zipfile.ZIP_DEFLATED)

    current_zip.close()
    current_buffer.seek(0)
    archives.append(current_buffer.getvalue())

    return archives


async def send_result(message: Message, archives: list[bytes], i18n: I18nContext,
                      has_unsupported: bool = False, filename: str | None = None) -> None:
    bot_info = await message.bot.me()
    base_filename = f"{filename} by @{bot_info.username}" if filename else f"@{bot_info.username}"
    caption = i18n.get("format-warning") if has_unsupported else None
    total = len(archives)

    for idx, data in enumerate(archives, 1):
        current_filename = f"{base_filename} (part {idx}).zip" if total > 1 else f"{base_filename}.zip"
        
        await message.reply_document(
            document=BufferedInputFile(data, filename=current_filename),
            caption=caption
        )
