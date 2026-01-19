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


async def setup_i18n() -> I18nMiddleware:
    i18n_core = FluentRuntimeCore(path="locales/{locale}")
    await i18n_core.startup()
    logger.info(f"Loaded locales: {i18n_core.available_locales}")
    return I18nMiddleware(core=i18n_core, default_locale="en")


def setup_middlewares(dp: Dispatcher, i18n: I18nMiddleware) -> None:
    dp.update.middleware(LocaleMiddleware())
    dp.callback_query.middleware(LocaleMiddleware())
    dp.message.middleware(LocaleMiddleware())
    dp.message.middleware(RateLimitMiddleware())
    dp.callback_query.middleware(RateLimitMiddleware())
    
    i18n.setup(dispatcher=dp)


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

    i18n = await setup_i18n()

    dp = Dispatcher()
    
    for router in [start_router, help_router, packs.router, emoji.router, 
                   stickers.router, fallback.router]:
        dp.include_router(router)
    
    setup_middlewares(dp, i18n)

    try:
        await dp.start_polling(
            bot,
            polling_timeout=30,
            handle_as_tasks=True,
            tasks_concurrency_limit=100,
            close_bot_session=True,
        )
    finally:
        await i18n.core.shutdown()
        await bot.session.close()
        await close_db()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        pass
    except Exception as e:
        logger.exception(f"Unexpected error: {e}")
