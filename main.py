import asyncio

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.types import BotCommand
from aiogram_i18n import I18nMiddleware
from aiogram_i18n.cores.fluent_runtime_core import FluentRuntimeCore

from bot.commands import start_router, help_router
from bot.core import logger, setup_logging, config
from bot.database import init_db, close_db
from bot.handlers import emoji, stickers, packs, fallback
from bot.middlewares import LocaleMiddleware, RateLimitMiddleware


async def set_bot_commands(bot: Bot) -> None:
    commands = [
        BotCommand(command="start", description="🚀 Start the bot"),
        BotCommand(command="help", description="❓ Show help information"),
    ]
    await bot.set_my_commands(commands)


async def main() -> None:
    setup_logging()

    await init_db()

    bot = Bot(
        token=config.BOT_TOKEN,
        default=DefaultBotProperties(
            parse_mode=ParseMode.HTML,
            link_preview_is_disabled=True
        )
    )

    await set_bot_commands(bot)

    dp = Dispatcher()

    for router in [start_router, help_router, packs.router, emoji.router, stickers.router, fallback.router]:
        dp.include_router(router)

    i18n = I18nMiddleware(
        core=FluentRuntimeCore(path="locales/{locale}"),
        default_locale="en"
    )
    i18n.setup(dispatcher=dp)

    dp.update.middleware(LocaleMiddleware())
    dp.message.middleware(LocaleMiddleware())
    dp.callback_query.middleware(LocaleMiddleware())
    dp.message.middleware(RateLimitMiddleware())
    dp.callback_query.middleware(RateLimitMiddleware())

    try:
        await dp.start_polling(bot, skip_updates=True)
    finally:
        await bot.session.close()
        await close_db()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        pass
    except Exception as e:
        logger.exception(f"Unexpected error: {e}")
