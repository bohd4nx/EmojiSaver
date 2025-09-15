import logging

from .bot import TelegramBot
from .userbot import UserBot

logger = logging.getLogger(__name__)


class EmojiDownloaderApp:
    def __init__(self) -> None:
        self.bot = TelegramBot()
        self.userbot = UserBot()

    async def start(self) -> None:
        try:
            logger.info("Starting Emoji Downloader Bot...")

            await self.userbot.start()
            logger.info("Logged in as @%s [%s]", self.userbot.username, self.userbot.user_id)

            await self.bot.setup()
            logger.info("Bot setup completed")

            await self.bot.start_polling()

        except Exception as e:
            logger.error(f"Failed to start application: {e}")
            await self.shutdown()
            raise
        finally:
            await self.shutdown()

    async def shutdown(self) -> None:
        logger.info("Shutting down...")
        await self.userbot.stop()
        await self.bot.close()
        logger.info("Shutdown completed")


app = EmojiDownloaderApp()
