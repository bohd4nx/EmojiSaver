import configparser
import logging
import sys
from pathlib import Path

logger = logging.getLogger(__name__)


class Config:
    def __init__(self):
        self.parser = configparser.ConfigParser()
        self._load_config()
        self._setup_properties()
        self._validate_config()

    def _load_config(self) -> None:
        config_path = Path(__file__).parent.parent.parent / 'config.ini'
        try:
            self.parser.read(config_path, encoding='utf-8-sig')
        except Exception:
            logger.error("Failed to read config file")
            sys.exit(1)

    def _setup_properties(self) -> None:
        self.BOT_TOKEN = self.parser.get('Bot', 'BOT_TOKEN', fallback='').strip()

    def _validate_config(self) -> None:
        if not self.BOT_TOKEN:
            logger.error("Missing required config field: Bot > BOT_TOKEN")
            sys.exit(1)


config = Config()
