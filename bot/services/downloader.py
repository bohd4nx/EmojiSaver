from pathlib import Path

import filetype
from aiogram import Bot
from aiogram.exceptions import TelegramBadRequest

from bot.core import logger
from bot.services import tgs_to_json, tgs_to_lottie, tgs_to_png

# Non-convertible formats (video stickers, static images)
NON_CONVERTIBLE = {'webm', 'webp', 'mp4', 'gif', 'png', 'jpg', 'jpeg', 'mkv'}
# TGS format can be converted


def detect_format(data: bytes, fallback_path: str = '') -> str:
    # Check for TGS (gzipped JSON) first - filetype doesn't recognize it
    if len(data) >= 2 and data[:2] == b'\x1f\x8b':
        return 'tgs'

    # Use the filetype library for everything else
    kind = filetype.guess(data)
    if kind is not None:
        return kind.extension

    # Fallback to Telegram's file path extension if available
    if fallback_path:
        ext = Path(fallback_path).suffix.lstrip('.').lower()
        if ext:
            return ext

    return 'dat'


async def download_and_convert(file_id: str, bot: Bot) -> tuple[dict[str, bytes], bool]:
    try:
        logger.debug(f"Starting download: file_id={file_id}")
        file_info = await bot.get_file(file_id)
        # logger.debug(f"File info: path={file_info.file_path}, size={file_info.file_size}")

        file_data = await bot.download_file(file_info.file_path)

        if not file_data:
            logger.warning(f"Failed to download file: {file_id}")
            return {}, False

        data = file_data.read()

        # Detect format: magic bytes → Telegram path → 'dat' fallback
        ext = detect_format(data, file_info.file_path)
        logger.debug(f"Downloaded: {len(data)} bytes, detected: {ext}")

        # Non-convertible format - return original file as-is (webm, webp, png, etc.)
        if ext in NON_CONVERTIBLE:
            logger.debug(f"Non-convertible format: {ext}")
            return {f"{file_id}.{ext}": data}, False

        # Try to convert TGS only if it's actually a TGS file
        if ext == 'tgs':
            json_data = await tgs_to_json(data)
            lottie_data = await tgs_to_lottie(data)
            png_data = await tgs_to_png(data)

            # Collect all files (original + successful conversions)
            files = {f"{file_id}.{ext}": data}
            files.update({k: v for k, v in {
                f"{file_id}.json": json_data,
                f"{file_id}.lottie": lottie_data,
                f"{file_id}.png": png_data
            }.items() if v})

            has_conversions = len(files) > 1
            logger.debug(f"Conversion complete: {len(files)} files, conversions: {has_conversions}")
            return files, not has_conversions
        
        # Unknown format - save as-is but warn
        logger.warning(f"Unknown format for conversion: {ext}")
        return {f"{file_id}.{ext}": data}, True 

    except TelegramBadRequest as e:
        if "wrong file_id" in str(e) or "temporarily unavailable" in str(e):
            logger.warning(f"File unavailable: {file_id}")
        else:
            logger.error(f"Telegram error for {file_id}: {e}")
        return {}, False
    except Exception as e:
        logger.exception(f"Failed to process {file_id}: {e}")
        return {}, False
