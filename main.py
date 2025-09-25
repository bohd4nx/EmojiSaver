import asyncio
import logging

from app.core.Bot import TelegramBot

logging.basicConfig(
    level=logging.ERROR,
    format='[%(asctime)s] - %(levelname)s: %(message)s',
    datefmt='%H:%M:%S'
)

logger = logging.getLogger(__name__)


async def run() -> None:
    bot = TelegramBot()
    
    try:
        logger.info("Starting Emoji Downloader Bot...")
        await bot.setup()
        await bot.start_polling()
    except KeyboardInterrupt:
        logger.info("Received interrupt signal")
    except Exception as e:
        logger.error(f"Application error: {e}")
    finally:
        await bot.close()


if __name__ == "__main__":
    asyncio.run(run())
