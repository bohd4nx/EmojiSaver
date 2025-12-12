import logging
from pathlib import Path

from rich.console import Console
from rich.logging import RichHandler


def setup_logging() -> None:
    log_file = Path("bot.log")
    console = Console()

    file_handler = logging.FileHandler(log_file, mode="w", encoding="utf-8")
    file_handler.setLevel(logging.DEBUG)

    console_handler = RichHandler(
        console=console,
        show_time=False,
        show_level=False,
        show_path=False,
        markup=True,
        rich_tracebacks=False,
        tracebacks_show_locals=False,
    )
    console_handler.setLevel(logging.INFO)

    logging.basicConfig(
        level=logging.DEBUG,
        format="[%(asctime)s] - %(levelname)s: %(message)s",
        datefmt="%d.%m.%y %H:%M:%S",
        handlers=[console_handler, file_handler],
        force=True
    )

    logging.getLogger("aiogram.dispatcher").setLevel(logging.INFO)
    logging.getLogger("aiogram.event").setLevel(logging.ERROR)


logger = logging.getLogger(__name__)
