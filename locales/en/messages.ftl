start-message = 
    👋 <b>Hello, {$name}!</b>
    
    Download and convert Telegram stickers and emoji to <code>TGS</code>, <code>JSON</code>, <code>Lottie</code>, and <code>PNG</code> formats.
    
    <b>🎯 What I can do:</b> [/help]
    • Extract custom (premium) emoji from messages
    • Convert stickers to editable formats
    • Download entire sticker/emoji packs
    
    📊 <b>Total downloads:</b> {$downloads}
    
    <b>💬 Quick start:</b> Send me emoji, sticker, or paste a pack link!
    
    ⭐️ <a href="{$github}">GitHub</a> • 👨‍💻 <a href="{$developer}">Developer</a>

help-message = 
    📖 <b>How to use:</b>
    
    1️⃣ <b>Custom Emoji:</b>
    • Send any message with custom (premium) emoji
    • All emoji will be extracted and converted automatically
    
    2️⃣ <b>Stickers:</b>
    • Send or forward any sticker
    • Converts to editable formats (JSON, Lottie, PNG)
    
    3️⃣ <b>Entire Packs:</b>
    • Paste a pack link: <code>https://t.me/addstickers/PackName</code>
    • Or emoji pack: <code>https://t.me/addemoji/PackName</code>
    • The entire pack will be downloaded and converted
    
    💡 <b>Tip:</b> For regular static emoji, use:
    <code>https://t.me/addemoji/StaticEmoji</code>
    <code>https://t.me/addstickers/StaticEmoji</code>
    
    📦 <b>Output formats:</b>
    • <code>.tgs</code> — Original Telegram format
    • <code>.json</code> — Uncompressed Lottie animation
    • <code>.lottie</code> — Compressed Lottie (LottieFiles format)
    • <code>.png</code> — Raster image (first frame, 512×512px)

format-warning = 
    ⚠️ <b>Format Notice</b>
    
    Some items could not be converted.
    Original files were saved as-is.

processing-error = 
    ❌ <b>Error:</b>
    
    <code>{$error}</code>
    
    Please try again.

invalid-input = 
    ❌ <b>Supported:</b>
    • Custom (premium) emoji
    • Stickers (any format)
    • Sticker/emoji pack links
    
    Type /help for instructions.

processing = ⏳ <b>Processing your request...</b>

processing-pack = ⏳ <b>Processing: {$current}/{$total}</b>

processing-failed = 
    ❌ <b>Processing failed</b>
    
    Try again later.

pack-not-found = 
    ❌ <b>Pack not found</b>
    
    Check the link and try again.

no-custom-emoji = 
    ❌ <b>Custom (premium) emoji not found</b>
    
    Send a message with custom emoji.

rate-limit-alert = 🔒 Please wait {$seconds} seconds before sending next request!
