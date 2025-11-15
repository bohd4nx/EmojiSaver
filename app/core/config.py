import os
import sys
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv

from app.core.logger import logger


class Config:
    def __init__(self):
        self._load_env()
        self._data = {
            "BOT_TOKEN": self._get_bot_token(),
            "THROTTLE_TIME": self._get_throttle_time(),
        }

    @staticmethod
    def _load_env():
        env_path = Path(__file__).parent.parent.parent / ".env"
        try:
            load_dotenv(env_path)
        except Exception as e:
            logger.error(f"Failed to load .env file: {e}")
            sys.exit(1)

    @staticmethod
    def _get_bot_token() -> str:
        token = os.getenv("BOT_TOKEN", "").strip()
        if not token:
            logger.error("Missing required environment variable: BOT_TOKEN")
            sys.exit(1)
        return token

    @staticmethod
    def _get_throttle_time() -> Optional[float]:
        raw = os.getenv("THROTTLE_TIME", "false").strip().lower()
        if raw == "false":
            return None
        try:
            return float(raw)
        except ValueError:
            return None

    def __getattr__(self, item):
        return self._data.get(item)


config = Config()
