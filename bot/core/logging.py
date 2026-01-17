import logging

from bot.__meta__ import APP_NAME


def setup_logging() -> None:
    formatter = logging.Formatter(
        fmt="[%(asctime)s] - %(levelname)s: %(message)s",
        datefmt="%d.%m.%y %H:%M:%S"
    )

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)

    file_handler = logging.FileHandler(
        f"{APP_NAME}.log",
        mode="w",
        encoding="utf-8"
    )
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    logging.basicConfig(
        level=logging.DEBUG,
        handlers=[console_handler, file_handler],
        force=True
    )

    logging.getLogger("aiogram.dispatcher").setLevel(logging.INFO)
    logging.getLogger("aiogram.event").setLevel(logging.ERROR)
    logging.getLogger("aiosqlite").setLevel(logging.WARNING)
    logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)


logger = logging.getLogger(__name__)
