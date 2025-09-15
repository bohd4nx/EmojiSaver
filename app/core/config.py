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
        self._setup_telegram()
        self._setup_bot()

    def _setup_telegram(self) -> None:
        api_id_str = self.parser.get('Telegram', 'API_ID', fallback='').strip()
        self.API_ID = int(api_id_str) if api_id_str.isdigit() else 0
        self.API_HASH = self.parser.get('Telegram', 'API_HASH', fallback='').strip()
        self.PHONE_NUMBER = self.parser.get('Telegram', 'PHONE_NUMBER', fallback='').strip()

    def _setup_bot(self) -> None:
        self.BOT_TOKEN = self.parser.get('Bot', 'BOT_TOKEN', fallback='').strip()

    def _validate_config(self) -> None:
        validation_rules = {
            "Telegram > API_ID": lambda: self.API_ID == 0,
            "Telegram > API_HASH": lambda: not self.API_HASH,
            "Telegram > PHONE_NUMBER": lambda: not self.PHONE_NUMBER,
            "Bot > BOT_TOKEN": lambda: not self.BOT_TOKEN
        }

        invalid_fields = [field for field, check in validation_rules.items() if check()]

        if invalid_fields:
            error_msg = f"Missing required config fields:\n" + '\n'.join(f'- {field}' for field in invalid_fields)
            logger.error(error_msg)
            sys.exit(1)


config = Config()
