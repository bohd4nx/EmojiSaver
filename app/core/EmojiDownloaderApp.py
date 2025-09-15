import logging

from .Bot import TelegramBot
from .UserBot import UserBot

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
            # logger.info("Bot setup completed")

            await self.bot.start_polling()

        except Exception as e:
            logger.error(f"Failed to start application: {e}")
            raise

    async def shutdown(self) -> None:
        logger.info("Shutting down...")
        try:
            await self.userbot.stop()
        except Exception as e:
            logger.error(f"Error stopping userbot: {e}")

        try:
            await self.bot.close()
        except Exception as e:
            logger.error(f"Error closing bot: {e}")

        logger.info("Shutdown completed")


app = EmojiDownloaderApp()
