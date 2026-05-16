from aiogram import Router

from .fallback import router as fallback_router

router = Router(name=__name__)
router.include_router(fallback_router)
