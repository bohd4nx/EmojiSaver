MESSAGES = {
    "start": """👋 <b>Hello, {name}</b>!

I can help you extract and download Telegram content in both <code>TGS</code> and <code>JSON</code> formats.

🔸 <b>What can I do?</b>
• Extract emoji from messages
• Convert <b>animated</b> stickers to editable format

Just send me any message with emoji or forward an <b>animated</b> sticker!

ℹ️ Use /help for more information""",

    "help": """1️⃣ <b>For Emoji:</b>
• Send any message containing custom emoji
• You'll receive all emoji extracted automatically

2️⃣ <b>For Animated Stickers:</b>
• Send or forward any <b>animated</b> sticker
• I'll convert it to editable format

📦 <b>Output:</b>
<code>.tgs</code> - Original Telegram format
<code>.json</code> - Lottie-compatible format for editing""",

    "loading": "⏳ Processing your request...",
    "no_emoji": "❌ <b>No custom emoji found</b> in your message.",
    "no_animated_sticker": "❌ Please send an <b>animated</b> sticker.",
    "success_tgs_only": "✅ <b>Partial success!</b>\n\n<code>.tgs</code> file ready but <code>.json</code> conversion failed.",
    "error": "❌ <b>Error:</b>\n\n<code>{error}</code>\n\nPlease try again.",
    "invalid_input": "❌ <b>Send only animated emoji or stickers</b>\n\nUse /help for instructions.",
    "processing_failed": "❌ <b>Processing failed. Try different emoji.</b>",
}
