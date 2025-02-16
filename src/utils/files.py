import logging
import os
import zipfile
from typing import List

from aiogram import types, Bot

from data.config import config
from .texts import Messages

logger = logging.getLogger(__name__)


def get_file_name(base_path: str, extension: str, index: int = None) -> str:
    if index is not None:
        return f"{base_path}({index}).{extension}"
    return f"{base_path}.{extension}"


def cleanup_files(files: List[str]) -> None:
    for file in files:
        try:
            if os.path.exists(file):
                os.remove(file)
        except Exception as e:
            logger.error(f"Error cleaning up file {file}: {e}")


async def create_archive(files: List[str], user_id: int, prefix: str, bot: Bot) -> str:
    os.makedirs(config.DOWNLOAD_DIR, exist_ok=True)
    bot_info = await bot.get_me()
    bot_username = bot_info.username or "bot"

    zip_path = os.path.join(
        config.DOWNLOAD_DIR,
        f"@{bot_username}_{user_id}_{prefix}.zip"
    )

    with zipfile.ZipFile(zip_path, 'w') as zipf:
        for file in files:
            zipf.write(file, os.path.basename(file))
    return zip_path


async def send_result(message: types.Message, zip_path: str, files_to_cleanup: List[str]) -> None:
    try:
        caption = None if len(files_to_cleanup) > 1 else Messages.SUCCESS_TGS_ONLY
        await message.reply_document(
            document=types.FSInputFile(zip_path),
            caption=caption
        )
    finally:
        cleanup_files(files_to_cleanup + [zip_path])
