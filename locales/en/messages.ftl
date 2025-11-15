start-message = 
    👋 <b>Hello, {$name}</b>!
    
    I can help you extract and download Telegram content in <code>TGS</code>, <code>JSON</code>, and <code>LOTTIE</code> formats.
    
    🔸 <b>What can I do?</b> [/help]
    • Extract emoji from messages
    • Convert <b>animated</b> stickers to editable format
    
    Just send me any message with emoji or forward an <b>animated</b> sticker!
    
    ⭐️ <a href="https://github.com/bohd4nx/EmojiSaver">GitHub</a> • 👨‍💻 <a href="https://t.me/bohd4nx">Developer</a>

help-message = 
    1️⃣ <b>For Emoji:</b>
    • Send any message containing custom emoji
    • You'll receive all emoji extracted automatically
    
    2️⃣ <b>For Animated Stickers:</b>
    • Send or forward any <b>animated</b> sticker
    • I'll convert it to editable format
    
    📦 <b>Output formats:</b>
    <code>.tgs</code> - Original Telegram format
    <code>.json</code> - Lottie format for editing
    <code>.lottie</code> - LottieFiles format (compressed)

format-warning = 
    ⚠️ <b>Format Notice:</b>
    
    Some emoji/stickers are in <b>WebM/WebP</b> formats and cannot be converted to editable Lottie.
    
    Only the original <code>.tgs</code> files were included for these items.

error = 
    ❌ <b>Error:</b>
    
    <code>{$error}</code>
    
    Please try again.

invalid-input = 
    ❌ <b>Send only animated emoji or stickers</b>
    
    Use /help for instructions.

loading = ⏳ <b>Processing your request...</b>

processing-failed = ❌ <b>Processing failed. Please try again.</b>

no-emoji = ❌ <b>No suitable emoji found in your message.</b>

no-animated-sticker = ❌ Please send an <b>animated</b> sticker.

throttle-warning = 🔒 <b>Please wait {$seconds} seconds before sending next request.</b>
