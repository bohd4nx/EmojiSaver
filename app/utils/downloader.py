from typing import Dict

from app.core import logger
from app.utils.converter import tgs_to_json, tgs_to_lottie


async def download_and_convert(file_id: str, bot) -> tuple[Dict[str, bytes], bool]:
    try:
        logger.debug(f"Getting file info for: {file_id}")
        file_info = await bot.get_file(file_id)
        logger.debug(f"File info: path={file_info.file_path}, size={file_info.file_size}")

        file_data = await bot.download_file(file_info.file_path)

        if not file_data:
            logger.warning(f"Failed to download file: {file_id}")
            return {}, False

        data = file_data.read()
        logger.debug(f"Downloaded {len(data)} bytes")

        is_tgs = file_info.file_path.endswith('.tgs')
        logger.debug(f"File format: is_tgs={is_tgs}, path={file_info.file_path}")

        if is_tgs:
            json_data = await tgs_to_json(data)
            lottie_data = await tgs_to_lottie(data)

            files = {
                f"{file_id}.tgs": data,
                f"{file_id}.json": json_data or b"",
                f"{file_id}.lottie": lottie_data or b""
            }
            logger.debug(f"Converted to {len(files)} files")
            return files, False
        else:
            logger.warning(f"Non-TGS format detected: {file_id}: {file_info.file_path} ")
            return {f"{file_id}.tgs": data}, True

    except Exception as e:
        logger.exception(f"Failed to process {file_id}: {e}")
        return {}, False
