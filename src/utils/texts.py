from dataclasses import dataclass


@dataclass(frozen=True)
class Messages:
    START = (
        "👋 <b>Hello, {name}</b>!\n\n"
        "I can help you extract and download Telegram content in both "
        "<code>TGS</code> and <code>JSON</code> formats.\n\n"
        "🔸 <b>What can I do?</b>\n"
        "• Extract emoji from messages\n"
        "• Convert <b>animated</b> stickers to editable format\n\n"
        "Just send me any message with emoji or forward an <b>animated</b> sticker!\n\n"
        "ℹ️ Use /help for more information"
    )

    HELP = (
        "1️⃣ <b>For Emoji:</b>\n"
        "• Send any message containing custom emoji\n"
        "• You can send multiple emoji in one message\n"
        "• I'll extract and convert them all automatically\n\n"
        "2️⃣ <b>For Animated Stickers:</b>\n"
        "• Send or forward me any <b>animated</b> sticker\n"
        "• I'll convert it to editable format\n\n"
        "📦 <b>What you'll get:</b>\n"
        "You'll receive a ZIP archive containing:\n"
        "<code>.tgs</code> - Original Telegram sticker format\n"
        "<code>.json</code> - Ready for editing in After Effects or other Lottie-compatible software\n\n"
    )

    LOADING = "⏳ Processing your request..."
    NO_EMOJI = "❌ <b>Oops!</b>\n\nI couldn't find any custom emoji in your message."
    NO_ANIMATED_STICKER = "❌ <b>Oops!</b>\n\nPlease send me an <b>animated</b> sticker!"
    # SUCCESS = "✅ <b>Success!</b>\n\nI've prepared your files!"
    SUCCESS_TGS_ONLY = "✅ <b>Partial success!</b>\n\nI've prepared the <code>.tgs</code> file but <code>.json</code> conversion failed :("
    ERROR = "❌ <b>Error occurred:</b>\n\n<code>{error}</code>\n\nPlease try again or contact dev if the issue persists."
    INVALID_INPUT = (
        "❌ <b>Invalid input! Send me only:</b>"
        "• <b>Animated</b> emoji\n"
        "• <b>Animated</b> sticker\n\n"
        "Use /help to learn how to use me properly"
    )


@dataclass(frozen=True)
class LogMessages:
    # CONVERSION_SUCCESS = "Successfully converted {path} to JSON format"
    CONVERSION_ERROR = "Failed to convert TGS to JSON: {error}"


@dataclass(frozen=True)
class Buttons:
    GITHUB = "🌟 GitHub"
    GITHUB_URL = "https://github.com/bohd4nx/EmojiSaver"

    DEVELOPER = "👨‍💻 Developer"
    DEVELOPER_URL = "https://t.me/bohd4nx"
