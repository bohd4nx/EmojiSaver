# Fallback language when the user has no locale or it is not supported.
DEFAULT_LOCALE = "en"

# List of allowed locales to ensure only bundled translations are used.
SUPPORTED_LOCALES = frozenset({"en", "ru"})

# Log file name to centralize logging configuration.
LOG_FILE_NAME = "Bot.log"

# Database file name to keep storage configuration consistent.
DATABASE_FILE_NAME = "EmojiSaverBot.db"

# Maximum allowed archive size to prevent oversized uploads.
MAX_ARCHIVE_SIZE = 45 * 1024 * 1024  # 45 MB

# File formats that should not be processed or converted by the system.
NON_CONVERTIBLE_FORMATS = frozenset(
    {"webm", "webp", "mp4", "gif", "png", "jpg", "jpeg", "mkv"}
)

# Metadata for exported Lottie animations to keep generation details consistent.
LOTTIE_MANIFEST = {
    "version": "2026.2.0",
    "generator": "EmojiSaverBot",
    "author": "https://github.com/bohd4nx",
    "description": (
        "Telegram bot for extracting and converting animated emoji "
        "and stickers into Lottie/JSON/TGS formats"
    ),
    "generator_url": "https://github.com/bohd4nx/EmojiSaver",
    "created": "via https://t.me/EmojiSaverBot",
    "revision": 1,
    "animations": [{"id": "animation", "direction": 1, "speed": 1, "layers": []}],
}
