import argparse
import asyncio

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram_i18n import I18nMiddleware
from aiogram_i18n.cores.fluent_compile_core import FluentCompileCore

from bot.commands import help_router, start_router
from bot.core import config, logger, setup_bot_profile, setup_logging
from bot.core.constants import DEFAULT_LOCALE
from bot.database import close_db, init_db
from bot.handlers import emoji, errors, packs, stickers
from bot.handlers.errors import setup_error_handlers
from bot.middlewares import (
    DatabaseMiddleware,
    LocaleMiddleware,
    RateLimitMiddleware,
)


async def main(setup: bool = False) -> None:
    setup_logging()
    await init_db()

    bot = Bot(
        token=config.BOT_TOKEN,
        default=DefaultBotProperties(
            parse_mode=ParseMode.HTML,
            link_preview_is_disabled=True,
        ),
    )

    if setup:
        # push commands, descriptions and short descriptions to Telegram, then exit
        await setup_bot_profile(bot)
        logger.info("Bot updated successfully.")
        await bot.session.close()
        return

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
    parser = argparse.ArgumentParser(description="EmojiSaver Telegram bot")
    parser.add_argument(
        "--setup",
        action="store_true",
        help="push bot commands/descriptions to Telegram and exit",
    )
    args = parser.parse_args()

    try:
        asyncio.run(main(setup=args.setup))
    except (KeyboardInterrupt, SystemExit):
        pass
    except Exception as exc:
        logger.exception("Unexpected error: %s", exc)
