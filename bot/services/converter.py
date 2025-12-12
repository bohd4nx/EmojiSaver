import gzip
import io
import json
import zipfile
from typing import Optional

import cairosvg
from lottie.exporters.svg import export_svg
from lottie.parsers.tgs import parse_tgs

from bot import __meta__
from bot.core import logger


def _create_lottie_manifest() -> dict:
    return {
        "version": __meta__.__version__,
        "generator": __meta__.__title__,
        "author": __meta__.__developer__,
        "description": __meta__.__description__,
        "generator_url": __meta__.__github__,
        "created": f"via {__meta__.__telegram__}",
        "revision": 1,
        "animations": [{
            "id": "animation",
            "direction": 1,
            "speed": 1,
            "layers": []
        }]
    }


def _tgs_to_svg_string(tgs_data: bytes) -> str:
    json_data = gzip.decompress(tgs_data)
    animation = parse_tgs(io.BytesIO(json_data))
    svg_buffer = io.StringIO()
    export_svg(animation, svg_buffer, frame=0)
    return svg_buffer.getvalue()


async def tgs_to_json(tgs_data: bytes) -> Optional[bytes]:
    try:
        result = gzip.decompress(tgs_data)
        logger.debug(f"TGS to JSON: {len(result)} bytes")
        return result
    except Exception as e:
        logger.error(f"TGS to JSON conversion failed: {e}")
        return None


async def tgs_to_lottie(tgs_data: bytes) -> Optional[bytes]:
    try:
        json_data = gzip.decompress(tgs_data)
        logger.debug(f"Decompressed TGS data: {len(json_data)} bytes")
        
        manifest = _create_lottie_manifest()
        
        lottie_buffer = io.BytesIO()
        with zipfile.ZipFile(lottie_buffer, 'w', zipfile.ZIP_DEFLATED) as zf:
            zf.writestr('manifest.json', json.dumps(manifest))
            zf.writestr('animations/animation.json', json_data)
        
        result = lottie_buffer.getvalue()
        logger.debug(f"TGS to Lottie: {len(result)} bytes")
        return result
    except Exception as e:
        logger.error(f"TGS to Lottie failed: {e}")
        return None


async def tgs_to_svg(tgs_data: bytes) -> Optional[bytes]:
    try:
        svg_data = _tgs_to_svg_string(tgs_data)
        result = svg_data.encode('utf-8')
        logger.debug(f"TGS to SVG: {len(result)} bytes")
        return result
    except Exception as e:
        logger.error(f"TGS to SVG failed: {e}")
        return None


async def tgs_to_png(tgs_data: bytes, width: int = 512, height: int = 512) -> Optional[bytes]:
    try:
        svg_data = _tgs_to_svg_string(tgs_data)
        png_data = cairosvg.svg2png(
            bytestring=svg_data.encode('utf-8'),
            output_width=width,
            output_height=height
        )
        logger.debug(f"TGS to PNG: {len(png_data)} bytes")
        return png_data
    except Exception as e:
        logger.error(f"TGS to PNG failed: {e}")
        return None