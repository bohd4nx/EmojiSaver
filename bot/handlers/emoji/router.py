from aiogram import Router

from .extract import router as extract_router

router = Router(name=__name__)
router.include_router(extract_router)
