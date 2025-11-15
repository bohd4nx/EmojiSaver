import asyncio

from aiogram import Bot, Dispatcher, types
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram_i18n import I18nMiddleware
from aiogram_i18n.cores.fluent_runtime_core import FluentRuntimeCore

from app.commands import register_start_handlers, register_help_handlers
from app.core import config, logger
from app.handlers import (
    register_emoji_handlers,
    register_sticker_handlers,
    register_fallback_handlers
)


async def main():
    bot = Bot(
        token=config.BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML, link_preview_is_disabled=True)
    )
    dp = Dispatcher(storage=MemoryStorage())

    try:
        i18n_middleware = I18nMiddleware(
            core=FluentRuntimeCore(path="locales/{locale}"),
            default_locale="en"
        )
        i18n_middleware.setup(dispatcher=dp)

        register_start_handlers(dp)
        register_help_handlers(dp)
        register_emoji_handlers(dp)
        register_sticker_handlers(dp)
        register_fallback_handlers(dp)

        commands = [
            types.BotCommand(command="start", description="🚀 Start the bot"),
            types.BotCommand(command="help", description="❓ Show help information")
        ]
        await bot.set_my_commands(commands)

        await dp.start_polling(bot)
    except KeyboardInterrupt:
        logger.info("Received interrupt signal")
    except Exception as e:
        logger.error(f"Application error: {e}")
    finally:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())
