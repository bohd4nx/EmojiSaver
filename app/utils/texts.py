MESSAGES = {
    "start": """👋 <b>Hello, {name}</b>!

I can help you extract and download Telegram content in <code>TGS</code>, <code>JSON</code>, and <code>LOTTIE</code> formats.

🔸 <b>What can I do?</b> [/help]
• Extract emoji from messages
• Convert <b>animated</b> stickers to editable format

Just send me any message with emoji or forward an <b>animated</b> sticker!

⭐️ <a href="https://github.com/bohd4nx/EmojiSaver">GitHub</a> • 👨‍💻 <a href="https://t.me/bohd4nx">Developer</a>""",

    "help": """1️⃣ <b>For Emoji:</b>
• Send any message containing custom emoji
• You'll receive all emoji extracted automatically

2️⃣ <b>For Animated Stickers:</b>
• Send or forward any <b>animated</b> sticker
• I'll convert it to editable format

📦 <b>Output formats:</b>
<code>.tgs</code> - Original Telegram format
<code>.json</code> - Lottie format for editing
<code>.lottie</code> - LottieFiles format (compressed)""",

    "loading": "⏳ Processing your request...",
    "no_emoji": "❌ <b>No custom emoji found</b> in your message.",
    "no_animated_sticker": "❌ Please send an <b>animated</b> sticker.",
    "error": "❌ <b>Error:</b>\n\n<code>{error}</code>\n\nPlease try again.",
    "invalid_input": "❌ <b>Send only animated emoji or stickers</b>\n\nUse /help for instructions.",
    "processing_failed": "❌ <b>Processing failed. Try different emoji.</b>",
}
