import gzip
import io
import json
import zipfile

from rlottie_python import LottieAnimation  # type: ignore[attr-defined]

from bot.core import logger
from bot.core.constants import LOTTIE_MANIFEST


async def tgs_to_json(tgs_data: bytes) -> bytes | None:
    try:
        return gzip.decompress(tgs_data)
    except Exception as exc:
        logger.error("TGS to JSON failed: %s", exc)
        return None


async def tgs_to_lottie(tgs_data: bytes) -> bytes | None:
    try:
        json_data = gzip.decompress(tgs_data)
        buffer = io.BytesIO()
        with zipfile.ZipFile(buffer, "w", zipfile.ZIP_DEFLATED) as zf:
            zf.writestr("manifest.json", json.dumps(LOTTIE_MANIFEST))
            zf.writestr("animations/animation.json", json_data)
        return buffer.getvalue()
    except Exception as exc:
        logger.error("TGS to Lottie failed: %s", exc)
        return None


async def tgs_to_png(tgs_data: bytes, width: int = 512, height: int = 512) -> bytes | None:
    try:
        json_str = gzip.decompress(tgs_data).decode("utf-8")
        anim = LottieAnimation.from_data(json_str)
        img = anim.render_pillow_frame(frame_num=0, width=width, height=height)
        buffer = io.BytesIO()
        img.save(buffer, format="PNG")
        return buffer.getvalue()
    except Exception as exc:
        logger.error("TGS to PNG failed: %s", exc)
        return None
