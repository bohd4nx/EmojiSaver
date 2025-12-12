import logging
import os
import sys
from pathlib import Path

from dotenv import load_dotenv

logger = logging.getLogger(__name__)


class Config:
    def __init__(self):
        env_path = Path(__file__).resolve().parents[2] / ".env"

        if not env_path.exists():
            logger.error(".env file not found!")
            sys.exit(1)

        load_dotenv(env_path)

        if not os.getenv("BOT_TOKEN"):
            logger.error("Missing required env variable: BOT_TOKEN")
            sys.exit(1)

        self.BOT_TOKEN = os.getenv("BOT_TOKEN")
        self.RATE_LIMIT_COOLDOWN = int(os.getenv("RATE_LIMIT_COOLDOWN", 5))


config = Config()
