import gzip
import io
import json
import zipfile

from rlottie_python import LottieAnimation

from bot.__meta__ import VERSION, TITLE, DESCRIPTION, GITHUB_URL, TELEGRAM_URL, DEVELOPER_URL
from bot.core import logger


def _create_lottie_manifest() -> dict:
    return {
        "version": VERSION,
        "generator": TITLE,
        "author": DEVELOPER_URL,
        "description": DESCRIPTION,
        "generator_url": GITHUB_URL,
        "created": f"via {TELEGRAM_URL}",
        "revision": 1,
        "animations": [{
            "id": "animation",
            "direction": 1,
            "speed": 1,
            "layers": []
        }]
    }


async def tgs_to_json(tgs_data: bytes) -> bytes | None:
    try:
        return gzip.decompress(tgs_data)
    except Exception as e:
        logger.error(f"TGS to JSON failed: {e}")
        return None


async def tgs_to_lottie(tgs_data: bytes) -> bytes | None:
    try:
        json_data = gzip.decompress(tgs_data)
        manifest = _create_lottie_manifest()

        lottie_buffer = io.BytesIO()
        with zipfile.ZipFile(lottie_buffer, 'w', zipfile.ZIP_DEFLATED) as zf:
            zf.writestr('manifest.json', json.dumps(manifest))
            zf.writestr('animations/animation.json', json_data)

        return lottie_buffer.getvalue()
    except Exception as e:
        logger.error(f"TGS to Lottie failed: {e}")
        return None


async def tgs_to_png(tgs_data: bytes, width: int = 512, height: int = 512) -> bytes | None:
    try:
        json_data = gzip.decompress(tgs_data)
        json_str = json_data.decode('utf-8')
        anim = LottieAnimation.from_data(json_str)

        img = anim.render_pillow_frame(frame_num=0, width=width, height=height)
        buffer = io.BytesIO()
        img.save(buffer, format='PNG')

        return buffer.getvalue()
    except Exception as e:
        logger.error(f"TGS to PNG failed: {e}")
        return None
