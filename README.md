<div align="center">
  <img src="icon.svg" alt="Emoji Saver Bot Logo" width="120" height="120" style="border-radius: 24px;">

  <h1 style="margin-top: 24px;">Telegram Emoji Saver Bot</h1>

  <p style="font-size: 18px; color: #666; margin-bottom: 24px;">
    <strong>Extract and convert Telegram animated emoji & stickers to editable formats</strong>
  </p>

  <p>
    <a href="https://github.com/bohd4nx/EmojiSaver/issues">Report Bug</a>
    ·
    <a href="https://github.com/bohd4nx/EmojiSaver/issues">Request Feature</a>
    ·
    <a href="https://t.me/EmojiSaverBot">Demo Bot</a>
  </p>

</div>

## Features

- **Download Stickers** - Download and convert any Telegram sticker
- **Extract Premium Emoji** - Extract custom emoji from messages
- **Full Pack Download** - Download entire sticker/emoji packs from t.me links
- **Smart Format Detection** - Auto-detect file format (TGS, WebM, WebP, etc.)
- **Multi-Part Archives** - Auto-split large packs into 45 MB parts
- **Batch Processing** - Handle multiple items with progress tracking
- **Multi-Language** - English and Russian support

## Quick Start

### 1. Installation

```bash
git clone https://github.com/bohd4nx/EmojiSaver.git
cd EmojiSaver
pip install -r requirements.txt
```

### 2. Configuration

Create `.env` file in project root:

```env
# Your bot token, get it from @BotFather
BOT_TOKEN=1234567890:your_bot_token_from_@botfather

# Rate limit cooldown in seconds (default: 5)
RATE_LIMIT_COOLDOWN=5
```

### 3. Run

```bash
python main.py
```

## Usage

### Bot Commands

- `/start` - Welcome message and instructions
- `/help` - Detailed usage guide

### Custom Emoji Extraction

1. **Forward or send** message with an animated custom emoji
2. **Wait** for processing
3. **Download** ZIP archive with all formats
4. **Edit** in your favorite animation software

### Sticker Conversion

1. **Forward or send** any sticker to bot
2. **Wait** for processing
3. **Download** ZIP archive with converted formats (or original file)
4. **Use** in After Effects, Figma, or LottieFiles

### Pack Download

1. **Send pack URL** (e.g., `https://t.me/addstickers/YourPack` or `https://t.me/addemoji/YourPack`)
2. **Watch progress** as bot processes each item
3. **Download** complete archive with all stickers/emoji converted
4. **Edit** entire pack in your workflow

> **💡 Tip:** For regular static emoji, use the StaticEmoji pack:  
> `https://t.me/addemoji/StaticEmoji` or `https://t.me/addstickers/StaticEmoji`

## Format Compatibility

### Output Formats

| Format     | Extension | Software Compatibility                        | Use Case                             |
| ---------- | --------- | --------------------------------------------- | ------------------------------------ |
| **TGS**    | `.tgs`    | Telegram                                      | Upload as custom emoji/stickers      |
| **JSON**   | `.json`   | Adobe After Effects, Figma, Lottie Web Player | Edit animations, web implementation  |
| **PNG**    | `.png`    | Photoshop, GIMP, Any image viewer             | Raster preview, 512x512 pixels       |
| **Lottie** | `.lottie` | LottieFiles, Android/iOS apps                 | Cross-platform animation integration |

### Input Requirements

- **Type**: Any Telegram sticker or custom emoji
- **Supported Formats**: 
  - TGS (Lottie-based animations) - **converted** to JSON, Lottie, PNG
  - WebM, WebP, MP4, GIF - **saved as original** without conversion

2. **Download** - Retrieve TGS files from Telegram servers
3. **Decompression** - Extract Lottie JSON from gzipped TGS
4. **Conversion** - Create JSON, Lottie, APNG, and PNG formats
5. **Packaging** - Compress files into ZIP archives (max 45 MB per part)
6. **Delivery** - Send back to user with multi-part support if needed

---

<div align="center">

### Made with ❤️ by [@bohd4nx](https://t.me/bohd4nx)

**Star ⭐ this repo if you found it useful!**

</div>
