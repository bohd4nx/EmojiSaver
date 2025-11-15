from .emoji import register_emoji_handlers
from .fallback import register_fallback_handlers
from .stickers import register_sticker_handlers

__all__ = [
    'register_emoji_handlers',
    'register_sticker_handlers',
    'register_fallback_handlers',
]
