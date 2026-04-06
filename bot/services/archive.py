import io
import random
import zipfile

from aiogram.enums import ChatAction
from aiogram.types import BufferedInputFile, Message
from aiogram_i18n import I18nContext

from bot.core.constants import MAX_ARCHIVE_SIZE


async def pack_zip(files: dict[str, bytes]) -> list[bytes]:
    archives = []
    current_buffer = io.BytesIO()
    current_zip = zipfile.ZipFile(current_buffer, "w", zipfile.ZIP_DEFLATED)

    for name, data in files.items():
        zip_path = f"{name.split('.')[0]}/{name}" if len(files) > 2 else name
        current_zip.writestr(zip_path, data)

        current_buffer.seek(0)
        if len(current_buffer.getvalue()) > MAX_ARCHIVE_SIZE:
            current_zip.close()
            archives.append(current_buffer.getvalue())

            current_buffer = io.BytesIO()
            current_zip = zipfile.ZipFile(current_buffer, "w", zipfile.ZIP_DEFLATED)

    current_zip.close()
    current_buffer.seek(0)
    archives.append(current_buffer.getvalue())

    return archives


async def send_result(
    message: Message,
    archives: list[bytes],
    i18n: I18nContext,
    has_unsupported: bool = False,
    filename: str | None = None,
) -> None:
    assert message.bot
    bot_info = await message.bot.me()
    base_name = (
        f"{filename} by @{bot_info.username}" if filename else f"@{bot_info.username}"
    )
    caption = i18n.get("format-warning") if has_unsupported else None
    total = len(archives)

    for idx, data in enumerate(archives, 1):
        zip_name = f"{base_name} (part {idx}).zip" if total > 1 else f"{base_name}.zip"
        await message.bot.send_chat_action(message.chat.id, ChatAction.UPLOAD_DOCUMENT)
        await message.reply_document(
            document=BufferedInputFile(data, filename=zip_name),
            caption=caption,
        )

    # Show donate message with ~25% probability (approximately every 4 downloads)
    if random.random() < 0.25:
        await message.answer(i18n.get("donate-message"))
