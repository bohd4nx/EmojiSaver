import logging
import os
import shutil
from typing import List

from aiogram import types, Bot
from aiogram.types import WebAppInfo
from aiogram.utils.keyboard import InlineKeyboardBuilder

from data.config import config
from .db import db
from .texts import Messages, Buttons

logger = logging.getLogger(__name__)


def get_file_name(base_path: str, extension: str, file_id: str | None = None) -> str:
    os.makedirs(base_path, exist_ok=True)
    if file_id is None:
        raise ValueError("file_id is required")

    clean_id = file_id.replace('emoji(', '').replace(')', '')
    return os.path.join(base_path, f"{clean_id}.{extension}")


async def create_archive(files: List[str], user_id: int, bot: Bot) -> str:
    temp_dir = os.path.join(config.DOWNLOAD_DIR, f"temp_{user_id}")
    archive_name = f"@{(await bot.me()).username}"

    try:
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)
        os.makedirs(temp_dir)

        if len(files) <= 2:
            for file_path in files:
                shutil.copy2(
                    file_path,
                    os.path.join(temp_dir, os.path.basename(file_path))
                )
        else:
            for file_path in files:
                file_id = os.path.splitext(os.path.basename(file_path))[0]
                item_dir = os.path.join(temp_dir, f"[{file_id}]")
                os.makedirs(item_dir, exist_ok=True)
                shutil.copy2(file_path, os.path.join(item_dir, os.path.basename(file_path)))

        archive_path = os.path.join(config.DOWNLOAD_DIR, archive_name)
        return shutil.make_archive(archive_path, 'zip', temp_dir)

    except Exception as e:
        logger.error(f"Failed to create archive: {e}")
        raise
    finally:
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)


def cleanup_files(files: List[str]) -> None:
    for file in files:
        try:
            if os.path.exists(file):
                os.remove(file)
        except Exception as e:
            logger.error(f"Failed to cleanup {file}: {e}")


async def _generate_preview_url(message: types.Message) -> str:
    code = await db.get_animations_code(message.from_user.id, message.message_id)
    return f"https://api.bohd4n.me/search/{code}" if code else None


async def send_result(message: types.Message, zip_path: str, files_to_cleanup: List[str]) -> None:
    try:
        builder = InlineKeyboardBuilder()
        preview_url = await _generate_preview_url(message)
        if preview_url:
            builder.button(
                text=Buttons.PREVIEW,
                web_app=WebAppInfo(url=preview_url)
            )

        caption = None if len(files_to_cleanup) > 1 else Messages.SUCCESS_TGS_ONLY
        await message.reply_document(
            document=types.FSInputFile(zip_path),
            caption=caption,
            reply_markup=builder.as_markup()
        )
    finally:
        cleanup_files(files_to_cleanup + [zip_path])
