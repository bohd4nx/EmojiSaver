start-message = 
    👋 <b>Hello, {$name}</b>!
    
    I can help you extract and download Telegram content in <code>TGS</code>, <code>JSON</code>, and <code>LOTTIE</code> formats.
    
    🔸 <b>What can I do?</b> [/help]
    • Extract emoji from messages
    • Convert <b>animated</b> stickers to editable format
    • Download entire sticker/emoji packs
    
    📊 <b>Total downloads:</b> {$downloads}
    
    Just send me emoji, forward a sticker, or paste a pack link!
    
    ⭐️ <a href="{$github}">GitHub</a> • 👨‍💻 <a href="{$developer}">Developer</a>

help-message = 
    1️⃣ <b>For Emoji:</b>
    • Send or forward any message containing custom emoji
    • You'll receive all emoji extracted automatically
    
    2️⃣ <b>For Animated Stickers:</b>
    • Send or forward any <b>animated</b> sticker
    • I'll convert it to editable format
    
    3️⃣ <b>For Entire Packs:</b>
    • Send pack link: <code>https://t.me/addstickers/PackName</code>
    • Or emoji pack: <code>https://t.me/addemoji/PackName</code>
    • I'll download and convert the entire pack
    
    📦 <b>Output formats:</b>
    <code>.tgs</code> - Original Telegram format
    <code>.json</code> - Lottie format for editing
    <code>.lottie</code> - LottieFiles format (compressed)
    <code>.svg</code> - Vector image (first frame)
    <code>.png</code> - Raster image (512x512px)

format-warning = 
    ⚠️ <b>Format Notice:</b>
    
    Some emoji/stickers are in <b>WebM/WebP</b> formats and cannot be converted to editable Lottie.
    
    Only the original <code>.tgs</code> files were included for these items.

processing-error = 
    ❌ <b>Error:</b>
    
    <code>{$error}</code>
    
    Please try again.

invalid-input = 
    ❌ <b>Send only animated emoji or stickers</b>
    
    Use /help for instructions.

processing = ⏳ <b>Processing your request...</b>

processing-pack = ⏳ <b>Processing: {$current}/{$total}</b>

processing-failed = ❌ <b>Processing failed. Please try again.</b>

no-custom-emoji = ❌ <b>No suitable emoji found in your message.</b>

no-animated-sticker = ❌ Please send or forward an <b>animated</b> sticker.

rate-limit-alert = 🔒 Please wait {$seconds} seconds before sending next request!
