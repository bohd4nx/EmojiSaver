from pathlib import Path

from aiogram import Bot
from aiogram.exceptions import TelegramBadRequest
import filetype

from bot.core import logger
from bot.core.constants import NON_CONVERTIBLE_FORMATS
from bot.services import tgs_to_json, tgs_to_lottie, tgs_to_png


def detect_format(data: bytes, fallback_path: str = "") -> str:
    if len(data) >= 2 and data[:2] == b"\x1f\x8b":
        return "tgs"

    kind = filetype.guess(data)
    if kind is not None:
        return kind.extension

    if fallback_path:
        ext = Path(fallback_path).suffix.lstrip(".").lower()
        if ext:
            return ext

    return "dat"


async def _convert(
    file_id: str, ext: str, data: bytes
) -> tuple[dict[str, bytes], bool]:
    if ext in NON_CONVERTIBLE_FORMATS:
        return {f"{file_id}.{ext}": data}, True

    json_data = await tgs_to_json(data)
    lottie_data = await tgs_to_lottie(data)
    png_data = await tgs_to_png(data)

    files: dict[str, bytes] = {f"{file_id}.{ext}": data}
    files |= {
        k: v
        for k, v in {
            f"{file_id}.json": json_data,
            f"{file_id}.lottie": lottie_data,
            f"{file_id}.png": png_data,
        }.items()
        if v
    }

    return files, len(files) == 1


async def download_and_convert(file_id: str, bot: Bot) -> tuple[dict[str, bytes], bool]:
    try:
        file_info = await bot.get_file(file_id)
        file_data = await bot.download_file(file_info.file_path)

        if not file_data:
            logger.warning("Failed to download file: %s", file_id)
            return {}, False

        data = file_data.read()

        # Detect format: magic bytes → Telegram path → 'dat' fallback
        ext = detect_format(data, file_info.file_path)
        logger.debug("Downloaded %s: %s bytes, format=%s", file_id, len(data), ext)

        return await _convert(file_id, ext, data)

    except TelegramBadRequest as exc:
        if "wrong file_id" in str(exc) or "temporarily unavailable" in str(exc):
            logger.warning("File unavailable: %s", file_id)
        else:
            logger.error("Telegram error for %s: %s", file_id, exc)
        return {}, False
    except Exception:
        logger.exception("Failed to process %s", file_id)
        return {}, False
