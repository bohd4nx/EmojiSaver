<div align="center">

# Telegram Emoji & Sticker Downloader

[![Python](https://img.shields.io/badge/Python-3.11%2B-blue)](https://www.python.org/downloads/)
[![aiogram](https://img.shields.io/badge/aiogram-3.17.0-green)](https://docs.aiogram.dev/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

This Telegram bot allows users to extract and download animated emoji and stickers in both TGS (Telegram format) and
JSON (Lottie) formats, making them available for editing in animation software.

</div>

<p align="center">
  <a href="https://t.me/EmojiSaverBot">🤖 @EmojiSaverBot</a> |
  <a href="https://api.bohd4n.me">🌐 Web Interface</a>
</p>

</div>

## ✨ Features

- 🎯 **Extract Animated Emoji** - Download custom emoji from messages
- 🎭 **Convert Stickers** - Transform animated stickers to editable formats
- 🔄 **Multiple Emoji Support** - Process several emoji in a single message
- 📦 **Dual Format Export** - Get both TGS and JSON formats in one archive
- 👁️ **Live Preview** - View animations directly in Telegram

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
       
       # MongoDB connection string (optional)
       MONGO_URL: str = "mongodb://username:password@host:port"
   
   config = Config()
   ```

## 🚀 Usage

### Running the Bot

```bash
python main.py
```

### User Guide

| Command  | Description                |
|----------|----------------------------|
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

## 🧩 Development

Want to contribute? Great! Here's how:

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

<div align="center">
  <h4>Made with ❤️ by <a href="https://t.me/bohd4nx">@bohd4nx</a></h4>
  <p>
    <a href="https://github.com/bohd4nx/EmojiSaver">
      <img src="https://img.shields.io/github/stars/bohd4nx/EmojiSaverBot?style=social" alt="GitHub stars">
    </a>
  </p>
</div>
