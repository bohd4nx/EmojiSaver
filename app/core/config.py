import os
import sys
from pathlib import Path

from dotenv import load_dotenv

from app.core.logger import logger


class Config:
    def __init__(self):
        env_path = Path(__file__).parent.parent.parent / '.env'
        load_dotenv(env_path)

        self.BOT_TOKEN = os.getenv('BOT_TOKEN', '').strip()
        if not self.BOT_TOKEN:
            logger.error("Missing BOT_TOKEN in environment variables!")
            sys.exit(1)


config = Config()
