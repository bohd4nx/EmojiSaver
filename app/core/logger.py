import logging
import sys
from pathlib import Path


class Logger:
    def __init__(self):
        self.log_file = Path(__file__).parent.parent.parent / "EmojiSaver.log"
        self._setup_root()
        self._setup_file_logging()
        self._setup_console_logging()
        self.logger = logging.getLogger("app")  # stupid thing

    @staticmethod
    def _setup_root():
        root = logging.getLogger()
        root.setLevel(logging.DEBUG)

        for h in root.handlers[:]:
            root.removeHandler(h)

    def _setup_file_logging(self):
        file_handler = logging.FileHandler(self.log_file, mode='w', encoding='utf-8')
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(logging.Formatter(
            '[%(asctime)s] %(name)s - %(levelname)s: %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        ))
        logging.getLogger().addHandler(file_handler)

    @staticmethod
    def _setup_console_logging():
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(logging.Formatter(
            '[%(asctime)s] - %(levelname)s: %(message)s',
            datefmt='%H:%M:%S'
        ))

        aiogram_logger = logging.getLogger('aiogram.dispatcher')
        aiogram_logger.setLevel(logging.INFO)
        aiogram_logger.addHandler(console_handler)


logger = Logger()
