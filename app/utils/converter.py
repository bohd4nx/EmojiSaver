import io
import json
import logging
from typing import Optional

import lottie

logger = logging.getLogger(__name__)


async def convert_tgs_to_json(tgs_data: bytes) -> Optional[bytes]:
    try:
        tgs_buffer = io.BytesIO(tgs_data)
        animation = lottie.parsers.tgs.parse_tgs(tgs_buffer)
        json_data = json.dumps(animation.to_dict(), indent=2).encode('utf-8')
        return json_data
    except Exception as e:
        logger.error(f"TGS to JSON conversion failed: {e}")
        return None
