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

- **Extract Custom Emoji** - Automatically extract all custom animated emoji from messages
- **Convert Stickers** - Transform TGS animated stickers to editable formats
- **Download Entire Packs** - Download full sticker or emoji packs from t.me links
- **Multiple Export Formats** - Get TGS, JSON, Lottie, SVG, and PNG in one archive
- **Batch Processing** - Handle multiple emoji at once with progress tracking
- **Simple Usage** - Just send emoji, stickers, or pack URLs

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

# Request throttling (in seconds). Leave empty to disable
THROTTLE_TIME=3.0

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

### Animated Sticker Conversion

1. **Forward or send** animated sticker to bot
2. **Wait** for processing
3. **Download** ZIP archive with all formats
4. **Use** in After Effects, Figma, or LottieFiles

### Pack Download

1. **Send pack URL** (e.g., `https://t.me/addstickers/YourPack` or `https://t.me/addemoji/YourPack`)
2. **Watch progress** as bot processes each item
3. **Download** complete archive with all stickers/emoji converted
4. **Edit** entire pack in your workflow

## Format Compatibility

### Output Formats

| Format     | Extension | Software Compatibility                        | Use Case                             |
| ---------- | --------- | --------------------------------------------- | ------------------------------------ |
| **TGS**    | `.tgs`    | Telegram                                      | Upload as custom emoji/stickers      |
| **JSON**   | `.json`   | Adobe After Effects, Figma, Lottie Web Player | Edit animations, web implementation  |
| **SVG**    | `.svg`    | Illustrator, Inkscape, Figma                  | Vector editing, first frame preview  |
| **PNG**    | `.png`    | Photoshop, GIMP, Any image viewer             | Raster preview, 512x512 pixels       |
| **Lottie** | `.lottie` | LottieFiles, Android/iOS apps                 | Cross-platform animation integration |

### Input Requirements

- **Type**: Animated custom emoji or TGS stickers only
- **Format**: TGS (Lottie-based) animations
- **Note**: WebM/WebP video stickers are not supported for conversion

### Processing Algorithm

1. **Detection** - Identify custom emoji, animated stickers, or pack URLs
2. **Download** - Retrieve TGS files from Telegram servers
3. **Decompression** - Extract Lottie JSON from gzipped TGS
4. **Conversion** - Create JSON and LOTTIE package formats
5. **Packaging** - Compress all files into organized ZIP archive
6. **Delivery** - Send back to user with format notice and progress tracking

---

<div align="center">

### Made with ❤️ by [@bohd4nx](https://t.me/bohd4nx)

**Star ⭐ this repo if you found it useful!**

</div>
