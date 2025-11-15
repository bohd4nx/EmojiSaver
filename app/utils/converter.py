import gzip
import io
import json
import zipfile
from typing import Optional

from app.core import logger


async def tgs_to_json(tgs_data: bytes) -> Optional[bytes]:
    try:
        return gzip.decompress(tgs_data)
    except Exception as e:
        logger.error(f"TGS to JSON conversion failed: {e}")
        return None


async def tgs_to_lottie(tgs_data: bytes) -> Optional[bytes]:
    try:
        json_data = gzip.decompress(tgs_data)

        manifest = {
            "version": "2025.1.2",
            "generator": "EmojiSaver Bot by @bohd4nx",
            "author": "Telegram → @EmojiSaver",
            "description": "Converted from Telegram TGS format",
            "generator_url": "https://github.com/bohd4nx/EmojiSaver",
            "created": "via Telegram Bot @EmojiSaverBot",
            "revision": 1,
            "animations": [
                {
                    "id": "animation",
                    "direction": 1,
                    "speed": 1,
                    "layers": []
                }
            ]
        }

        lottie_buffer = io.BytesIO()
        with zipfile.ZipFile(lottie_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
            zip_file.writestr('manifest.json', json.dumps(manifest))
            zip_file.writestr('animations/animation.json', json_data)

        return lottie_buffer.getvalue()
    except Exception as e:
        logger.error(f"TGS to Lottie conversion failed: {e}")
        return None
