import asyncio
import logging

from app.core.EmojiDownloaderApp import app

logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] - %(levelname)s: %(message)s',
    datefmt='%H:%M:%S'
)


async def main() -> None:
    try:
        await app.start()
    except KeyboardInterrupt:
        logging.info("Received interrupt signal")
    except Exception as e:
        logging.error(f"Application error: {e}")
    finally:
        await app.shutdown()


if __name__ == "__main__":
    asyncio.run(main())
