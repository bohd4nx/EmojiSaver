import logging
import os
import sys
from pathlib import Path

from dotenv import load_dotenv

logger = logging.getLogger(__name__)


class Config:
    def __init__(self) -> None:
        env_path = Path(__file__).resolve().parents[2] / ".env"
        load_dotenv(env_path)

        if not os.getenv("BOT_TOKEN"):
            logger.error("Missing required env variable: BOT_TOKEN")
            sys.exit(1)

        self.BOT_TOKEN: str = os.getenv("BOT_TOKEN")  # type: ignore[assignment]
        self.RATE_LIMIT_COOLDOWN = int(os.getenv("RATE_LIMIT_COOLDOWN", 5))

        self.POSTGRES_USER: str = os.getenv("POSTGRES_USER", "postgres")
        self.POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD", "")
        self.POSTGRES_HOST: str = os.getenv("POSTGRES_HOST", "db")
        self.POSTGRES_PORT: str = os.getenv("POSTGRES_PORT", "5432")
        self.POSTGRES_DB: str = os.getenv("POSTGRES_DB", "emojisaver")


config = Config()
