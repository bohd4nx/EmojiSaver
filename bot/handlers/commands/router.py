from aiogram import Router

from .help import router as help_router
from .start import router as start_router

router = Router(name=__name__)
router.include_router(start_router)
router.include_router(help_router)
