<h1 align="center">🎭 Telegram Emoji & Sticker Downloader</h1>

<p align="center">
   <b>Extract and download Telegram animated emoji and stickers in multiple formats for editing in animation software.</b>
</p>

<div align="center">

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue)](https://www.python.org/downloads/)
[![aiogram](https://img.shields.io/badge/aiogram-3x-green)](https://docs.aiogram.dev/)

[Report Bug](https://github.com/bohd4nx/EmojiSaver/issues) · [Request Feature](https://github.com/bohd4nx/EmojiSaver/issues)

</div>

## ✨ Features

- 🎯 **Extract Custom Emoji** - Download animated emoji from messages
- 🎭 **Convert Animated Stickers** - Transform TGS to editable formats
- 🔄 **Batch Processing** - Handle multiple emoji at once
- 📦 **Triple Format Export** - Get TGS, JSON, and LOTTIE files

## 🚀 Quick Start

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

## 📱 Usage

### Bot Interactions

| Action                        | Description                                                                      |
| ----------------------------- | -------------------------------------------------------------------------------- |
| **Send Custom Emoji**         | Send any message with animated custom emoji - they'll be automatically extracted |
| **Forward Animated Stickers** | Forward any animated sticker (TGS) to convert it                                 |
| **Batch Processing**          | Send multiple emoji in one message to download them all at once                  |

### Custom Emoji Extraction

1. Find a message with custom animated emoji
2. Send or forward it to the bot
3. Bot automatically detects and processes all custom emoji
4. Download the ZIP archive with TGS, JSON, and LOTTIE files

### Animated Sticker Conversion

1. Forward any animated sticker to the bot
2. Bot converts the TGS file to multiple formats
3. Receive original TGS, converted JSON, and LOTTIE files

### Compatibility

| Format | Software Compatibility                               | Usage                                |
| ------ | ---------------------------------------------------- | ------------------------------------ |
| TGS    | Telegram                                             | Upload as custom emoji/stickers      |
| JSON   | Adobe After Effects, Figma, Lottie Web Player        | Edit animations, web implementation  |
| LOTTIE | LottieFiles, Android/iOS apps, Web animation players | Cross-platform animation integration |

## ⚙️ Technical Implementation

### Processing Features

- **In-Memory Processing**: Efficient file handling without disk writes during processing
- **Error Resilience**: Handles API rate limits and processing errors
- **Async/Await**: Fully asynchronous for optimal performance

### File Handling

1. **Download** - Retrieve TGS from Telegram servers
2. **Conversion** - Transform to multiple formats (.tgs | .json | .lottie)
3. **Compression** - Package files into ZIP archive
4. **Delivery** - Send archive back to user

---

<div align="center">

### Made with ❤️ by [@bohd4nx](https://t.me/bohd4nx)

**Star ⭐ this repo if you found it useful!**

</div>
