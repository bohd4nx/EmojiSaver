from dataclasses import dataclass


@dataclass(frozen=True)
class Messages:
    START = """👋 <b>Hello, {name}</b>!

I can help you extract and download Telegram content in both <code>TGS</code> and <code>JSON</code> formats.

🔸 <b>What can I do?</b>
• Extract emoji from messages
• Convert <b>animated</b> stickers to editable format

Just send me any message with emoji or forward an <b>animated</b> sticker!

ℹ️ Use /help for more information"""

    HELP = """1️⃣ <b>For Emoji:</b>
• Send any message containing custom emoji
• You can send multiple emoji in one message
• I'll extract and convert them all automatically

2️⃣ <b>For Animated Stickers:</b>
• Send or forward me any <b>animated</b> sticker
• I'll convert it to editable format

📦 <b>What you'll get:</b>
You'll receive a ZIP archive containing:
<code>.tgs</code> - Original Telegram sticker format
<code>.json</code> - Ready for editing in After Effects or other Lottie-compatible software"""

    LOADING = "⏳ Processing your request..."
    NO_EMOJI = "❌ <b>Oops!</b>\n\nI couldn't find any custom emoji in your message."
    NO_ANIMATED_STICKER = "❌ <b>Oops!</b>\n\nPlease send me an <b>animated</b> sticker!"
    SUCCESS_TGS_ONLY = "✅ <b>Partial success!</b>\n\nI've prepared the <code>.tgs</code> file but <code>.json</code> conversion failed :("
    ERROR = "❌ <b>Error occurred:</b>\n\n<code>{error}</code>\n\nPlease try again or contact dev if the issue persists."
    INVALID_INPUT = """❌ <b>Invalid input! Send me only:</b>
• <b>Animated</b> emoji
• <b>Animated</b> sticker

Use /help to learn how to use me properly"""
    PROCESSING_FAILED = "❌ <b>Failed to process emoji. Please try different ones.</b>"


@dataclass(frozen=True)
class LogMessages:
    CONVERSION_ERROR = "Failed to convert TGS to JSON: {error}"


@dataclass(frozen=True)
class Buttons:
    GITHUB = "🌟 GitHub"
    GITHUB_URL = "https://github.com/bohd4nx/EmojiSaver"
    DEVELOPER = "👨‍💻 Developer"
    DEVELOPER_URL = "https://t.me/bohd4nx"
