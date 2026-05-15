from aiogram import Router

from .download import router as download_router

router = Router(name=__name__)
router.include_router(download_router)
