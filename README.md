<div align="center">
  <img src="app/icon.svg" alt="Emoji Saver Bot Logo" width="120" height="120" style="border-radius: 24px;">

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

- Extract Custom Emoji - Automatically extract all custom animated emoji from messages
- Convert Stickers - Transform TGS animated stickers to editable formats
- Triple Export - Get TGS, JSON, and LOTTIE formats in one archive
- Batch Processing - Handle multiple emoji at once
- Multi-language - Supports English and Russian
- Simple Usage - Just send emoji or stickers, no complex commands

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
# Get token from @BotFather
BOT_TOKEN=your_bot_token_here
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

1. **Send message** with animated custom emoji
2. **Wait** for processing
3. **Download** ZIP archive with all formats
4. **Edit** in your favorite animation software

### Animated Sticker Conversion

1. **Forward** or send animated sticker to bot
2. **Receive** ZIP with TGS, JSON, and LOTTIE files
3. **Use** in After Effects, Figma, or LottieFiles

## Format Compatibility

### Output Formats

| Format     | Extension | Software Compatibility                        | Use Case                             |
| ---------- | --------- | --------------------------------------------- | ------------------------------------ |
| **TGS**    | `.tgs`    | Telegram                                      | Upload as custom emoji/stickers      |
| **JSON**   | `.json`   | Adobe After Effects, Figma, Lottie Web Player | Edit animations, web implementation  |
| **Lottie** | `.lottie` | LottieFiles, Android/iOS apps                 | Cross-platform animation integration |

### Input Requirements

- **Type**: Animated custom emoji or TGS stickers only
- **Format**: TGS (Lottie-based) animations
- **Note**: WebM/WebP video stickers are not supported for conversion

## Technical Implementation

### Processing Algorithm

1. **Detection** - Identify custom emoji or animated stickers
2. **Download** - Retrieve TGS file from Telegram servers
3. **Decompression** - Extract Lottie JSON from gzipped TGS
4. **Conversion** - Create JSON and LOTTIE package formats
5. **Packaging** - Compress all files into ZIP archive
6. **Delivery** - Send back to user with format notice

## Logging

Bot creates `EmojiSaver.log` file with detailed processing information:

- **Console**: INFO level (dispatcher events, errors)
- **File**: DEBUG level (full processing details)

---

<div align="center">

### Made with ❤️ by [@bohd4nx](https://t.me/bohd4nx)

**Star ⭐ this repo if you found it useful!**

</div>
