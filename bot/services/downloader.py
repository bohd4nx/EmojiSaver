from aiogram import Bot
from aiogram.exceptions import TelegramBadRequest

from bot.core import logger
from bot.services import tgs_to_json, tgs_to_lottie, tgs_to_apng, tgs_to_png


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
        logger.debug(f"Downloaded: {len(data)} bytes")

        is_tgs = file_info.file_path.startswith('stickers/') or file_info.file_path.endswith('.tgs')

        if not is_tgs:
            logger.warning(f"Unsupported format: {file_info.file_path}")
            return {f"{file_id}.tgs": data}, True

        json_data = await tgs_to_json(data)
        lottie_data = await tgs_to_lottie(data)
        apng_data = await tgs_to_apng(data)
        png_data = await tgs_to_png(data)

        files = {
            f"{file_id}.tgs": data,
            f"{file_id}.json": json_data or b"",
            f"{file_id}.lottie": lottie_data or b"",
            f"{file_id}.apng": apng_data or b"",
            f"{file_id}.png": png_data or b""
        }
        logger.debug(f"Conversion complete: {len(files)} files generated")
        return files, False

    except TelegramBadRequest as e:
        if "wrong file_id" in str(e) or "temporarily unavailable" in str(e):
            logger.warning(f"File unavailable: {file_id}")
        else:
            logger.error(f"Telegram error for {file_id}: {e}")
        return {}, False
    except Exception as e:
        logger.exception(f"Failed to process {file_id}: {e}")
        return {}, False
