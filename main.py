import asyncio

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.types import BotCommand
from aiogram_i18n import I18nMiddleware
from aiogram_i18n.cores.fluent_compile_core import FluentCompileCore

from bot.commands import help_router, start_router
from bot.core import config, logger, setup_logging
from bot.core.constants import DEFAULT_LOCALE
from bot.database import close_db, init_db
from bot.handlers import emoji, errors, packs, stickers
from bot.handlers.errors import setup_error_handlers
from bot.middlewares import (
    DatabaseMiddleware,
    LocaleMiddleware,
    RateLimitMiddleware,
)


async def main() -> None:
    setup_logging()
    await init_db()

    bot = Bot(
        token=config.BOT_TOKEN,
        default=DefaultBotProperties(
            parse_mode=ParseMode.HTML,
            link_preview_is_disabled=True,
        ),
    )

    await bot.set_my_commands(
        [
            BotCommand(command="start", description="🚀 Start the bot"),
            BotCommand(command="help", description="❓ Show help information"),
        ]
    )

    i18n_core = FluentCompileCore(path="locales/{locale}")
    await i18n_core.startup()

    dp = Dispatcher()
    dp.include_routers(
        start_router,
        help_router,
        packs.router,
        emoji.router,
        stickers.router,
        errors.router,
    )

    i18n = I18nMiddleware(core=i18n_core, default_locale=DEFAULT_LOCALE)
    i18n.setup(dispatcher=dp)

    dp.update.middleware(DatabaseMiddleware())
    dp.update.middleware(LocaleMiddleware())
    dp.update.middleware(RateLimitMiddleware())

    setup_error_handlers(dp)

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
        await close_db()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        pass
    except Exception as exc:
        logger.exception("Unexpected error: %s", exc)
