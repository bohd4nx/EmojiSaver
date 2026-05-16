from aiogram import Router

from .convert import router as convert_router

router = Router(name=__name__)
router.include_router(convert_router)
