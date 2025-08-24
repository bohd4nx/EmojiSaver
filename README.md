# Telegram Emoji & Sticker Downloader

<div align="center">

[![Python](https://img.shields.io/badge/Python-3.11%2B-blue)](https://www.python.org/downloads/)
[![aiogram](https://img.shields.io/badge/aiogram-3.17.0-blue)](https://docs.aiogram.dev/)
[![GitHub](https://img.shields.io/github/stars/bohd4nx/EmojiSaverBot?style=social&label=Stars)](https://github.com/bohd4nx/EmojiSaverBot)
[![License](https://img.shields.io/badge/License-MIT-blue)](LICENSE)
[![Demo](https://img.shields.io/badge/Demo-@EmojiSaverBot-blue)](https://t.me/EmojiSaverBot)

</div>

This Telegram bot allows users to extract and download animated emoji and stickers in both TGS (Telegram format) and
JSON (Lottie) formats, making them available for editing in animation software.

## ✨ Features

- 🎯 **Extract Animated Emoji** - Download custom emoji from messages
- 🎭 **Convert Stickers** - Transform animated stickers to editable formats
- 🔄 **Multiple Emoji Support** - Process several emoji in a single message
- 📦 **Dual Format Export** - Get both TGS and JSON formats in one archive

## 🛠 Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/bohd4nx/EmojiSaver.git
   cd EmojiSaverBot
   ```

2. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment**

   - Create or modify `data/config.py`:

   ```python
   from dataclasses import dataclass

   @dataclass(frozen=True)
   class Config:
       # API credentials from https://my.telegram.org/apps
       API_ID: str = "your_api_id"
       API_HASH: str = "your_api_hash"

       # Bot token from @BotFather
       BOT_TOKEN: str = "your_bot_token"

       # Phone number in international format
       PHONE_NUMBER: str = "+1234567890"

       # Directory for temporary files
       DOWNLOAD_DIR: str = "../temp"

   config = Config()
   ```

## 🚀 Usage

### Running the Bot

```bash
python main.py
```

### User Guide

| Command  | Description                |
| -------- | -------------------------- |
| `/start` | Initialize the bot         |
| `/help`  | Display usage instructions |

#### 📱 Using with Emoji

1. Send any message containing custom animated emoji
2. The bot will automatically extract and convert all emoji
3. Download the ZIP archive containing both formats

#### 🎭 Using with Stickers

1. Forward any animated sticker to the bot
2. The bot will convert it to editable format
3. Download and enjoy!

---

<div align="center">

#### Made with ❤️ by [@bohd4nx](https://t.me/bohd4nx)

</div>
