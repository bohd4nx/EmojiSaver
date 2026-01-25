start-message = 
    {$hello} <b>Hello, {$name}!</b>
    
    Download and convert Telegram stickers and emoji to <code>TGS</code>, <code>JSON</code>, <code>Lottie</code>, and <code>PNG</code> formats.
    
    <b>{$convert} What I can do:</b> [/help]
    • Extract custom (premium) emoji from messages
    • Convert stickers to editable formats
    • Download entire sticker/emoji packs
    
    {$download} <b>Total downloads:</b> {$downloads}
    
    <b>{$search} Quick start:</b> Send me emoji, sticker, or paste a pack link!
    
    {$github} <a href="{$github_link}"> GitHub</a> • {$telegram} <a href="{$developer}">Developer</a>

help-message = 
    {$info} <b>How to use:</b>
    
    {$one} <b>Custom Emoji:</b>
    • Send any message with custom (premium) emoji
    • All emoji will be extracted and converted automatically
    
    {$two} <b>Stickers:</b>
    • Send or forward any sticker
    • Converts to editable formats (JSON, Lottie, PNG)
    
    {$three} <b>Entire Packs:</b>
    • Paste a pack link: <code>https://t.me/addstickers/PackName</code>
    • Or emoji pack: <code>https://t.me/addemoji/PackName</code>
    • The entire pack will be downloaded and converted
    
    {$clue} <b>Tip:</b> For regular static emoji, use:
    <code>https://t.me/addemoji/StaticEmoji</code>
    <code>https://t.me/addstickers/StaticEmoji</code>
    
    {$box} <b>Output formats:</b>
    • <code>.tgs</code> — Original Telegram format
    • <code>.json</code> — Uncompressed Lottie animation
    • <code>.lottie</code> — Compressed Lottie (LottieFiles format)
    • <code>.png</code> — Raster image (first frame, 512×512px)

format-warning = 
    {$warning} <b>Format Notice</b>
    
    Some items could not be converted.
    Original files were saved as-is.

processing-error = 
    {$forbidden} <b>Error:</b>
    
    <code>{$error}</code>
    
    Please try again or contact {$telegram} <a href="{$developer}">developer</a>

processing = {$processing} <b>Processing your request...</b>

processing-pack = {$processing} <b>Processing: {$current}/{$total}</b>

processing-failed = 
    {$forbidden} <b>Processing failed</b>
    
    Try again later or contact {$telegram} <a href="{$developer}">developer</a>

pack-not-found = 
    {$forbidden} <b>Pack not found</b>
    
    Check the link and try again.

no-custom-emoji = 
    {$forbidden} <b>Custom (premium) emoji not found</b>
    
    Send a message with custom emoji.

rate-limit-alert = {$forbidden} Please wait {$seconds} seconds before sending next request!
