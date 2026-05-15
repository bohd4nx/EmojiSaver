from aiogram import Router

from . import commands, emoji, errors, packs, stickers

router = Router(name=__name__)
router.include_routers(
    commands.router,
    packs.router,
    emoji.router,
    stickers.router,
    errors.router,
)
