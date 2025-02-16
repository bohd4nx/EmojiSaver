import asyncio
import logging

from src.core.bot import EmojiDownloaderBot

logging.basicConfig(
    level=logging.ERROR,
    format='%(asctime)s - [%(name)s] - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)


async def main() -> None:
    bot = EmojiDownloaderBot()
    await bot.start()


if __name__ == "__main__":
    asyncio.run(main())
