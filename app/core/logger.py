import logging

logging.basicConfig(
    level=logging.INFO,  # DEBUG, ERROR
    format='[%(asctime)s] - %(levelname)s: %(message)s',
    datefmt='%H:%M:%S'
)

logging.getLogger('aiogram.dispatcher').setLevel(logging.INFO)
logging.getLogger('aiogram.event').setLevel(logging.ERROR)

logger = logging.getLogger(__name__)

# TODO: Create a log of ERROR and INFO in the console, and DEBUG + the rest in a .log file.
