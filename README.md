# Telegram Emoji & Sticker Downloader

<div align="center">

[![Python](https://img.shields.io/badge/Python-3.12%2B-blue)](https://www.python.org/downloads/)
[![aiogram](https://img.shields.io/badge/aiogram-3.x-blue)](https://docs.aiogram.dev/)

</div>

Extract and download Telegram animated emoji and stickers in TGS and JSON formats for editing in animation software.

## ✨ Features

- 🎯 **Extract Custom Emoji** - Download animated emoji from messages
- 🎭 **Convert Animated Stickers** - Transform TGS to editable formats
- 🔄 **Batch Processing** - Handle multiple emoji at once
- 📦 **Dual Format Export** - Get both TGS and JSON files

## 🚀 Quick Start

1. **Clone and install**
   ```bash
   git clone https://github.com/bohd4nx/EmojiSaver.git
   cd EmojiSaver
   pip install -r requirements.txt
   ```

2. **Configure** - Fill `config.ini`:
   ```ini
   [Bot]
   BOT_TOKEN = 1234567890:your_bot_token
   ```

3. **Run**
   ```bash
   python main.py
   ```

### How to Use

| Action                        | Description                                                                      |
|-------------------------------|----------------------------------------------------------------------------------|
| **Send Custom Emoji**         | Send any message with animated custom emoji - they'll be automatically extracted |
| **Forward Animated Stickers** | Forward any animated sticker (TGS) to convert it                                 |
| **Batch Processing**          | Send multiple emoji in one message to download them all at once                  |

#### 📱 Custom Emoji Extraction

1. Find a message with custom animated emoji
2. Send or forward it to the bot
3. Bot automatically detects and processes all custom emoji
4. Download the ZIP archive with TGS and JSON files

#### 🎭 Animated Sticker Conversion

1. Forward any animated sticker to the bot
2. Bot converts the TGS file to JSON (Lottie) format
3. Receive both original TGS and converted JSON files

### Output Formats

- **TGS**: Original Telegram format (can be used in Telegram)
- **JSON**: Lottie format (compatible with After Effects, Figma, web animations)

## ⚙️ Technical Details

- **Bot API Only**: Uses aiogram for Telegram Bot API access
- **In-Memory Processing**: Efficient file handling without disk writes during processing
- **Error Resilience**: Handles API rate limits and processing errors
- **Async/Await**: Fully asynchronous for optimal performance

---

<div align="center">

#### Made with ❤️ by [@bohd4nx](https://t.me/bohd4nx)

**Star ⭐ this repo if you found it useful!**

</div>
