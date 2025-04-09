import json
import logging
from typing import Optional

import lottie

from .texts import LogMessages

logger = logging.getLogger(__name__)


async def convert_tgs_to_json(tgs_path: str) -> Optional[str]:
    try:
        with open(tgs_path, 'rb') as f:
            animation = lottie.parsers.tgs.parse_tgs(f)

        json_path = tgs_path.replace('.tgs', '.json')
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(animation.to_dict(), f, indent=2)

        return json_path
    except Exception as e:
        logger.error(LogMessages.CONVERSION_ERROR.format(error=e))
        return None
