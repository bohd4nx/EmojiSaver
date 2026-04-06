<div align="center">

  <img src="https://www.bohd4n.dev/assets/projects/StickersDownloader.svg" alt="EmojiSaver" width="120" height="120">

  <h1>Telegram Emoji Saver Bot</h1>

  <p>
    <b>Telegram bot that downloads and converts custom emoji and stickers to TGS, JSON, Lottie, and PNG formats.</b>
  </p>

[![Python](https://img.shields.io/badge/Python-3.12+-3776AB?style=flat&logo=python&logoColor=white)](https://python.org)
[![Demo Bot](https://img.shields.io/badge/Demo-@EmojiSaverBot-2CA5E0?style=flat&logo=telegram&logoColor=white)](https://t.me/EmojiSaverBot)
[![Donate TON](https://img.shields.io/badge/Donate-TON-0098EA?style=flat&logo=ton&logoColor=white)](https://app.tonkeeper.com/transfer/UQCppfw5DxWgdVHf3zkmZS8k1mt9oAUYxQLwq2fz3nhO8No5)
[![Stars](https://img.shields.io/github/stars/bohd4nx/EmojiSaver?style=flat&color=yellow)](https://github.com/bohd4nx/EmojiSaver/stargazers)

[Report Bug](https://github.com/bohd4nx/EmojiSaver/issues) · [Request Feature](https://github.com/bohd4nx/EmojiSaver/issues)

</div>

---

## Features

- Extract custom (premium) emoji from messages
- Convert stickers to TGS, JSON, Lottie, and PNG formats
- Download full sticker and emoji packs via `t.me` links
- Auto-detect file format by magic bytes with extension fallback
- Auto-split large archives into 45 MB parts
- Progress updates during pack processing
- Multi-language support (English and Russian)

---

## Installation

```bash
git clone https://github.com/bohd4nx/EmojiSaver.git
cd EmojiSaver
pip install -r requirements.txt
cp .env.example .env
```

Edit `.env` with your credentials (see [Configuration](#configuration) below), then run:

```bash
python main.py
```

---

## Configuration

| Variable              | Description                                         |
| --------------------- | --------------------------------------------------- |
| `BOT_TOKEN`           | Bot token from [@BotFather](https://t.me/BotFather) |
| `RATE_LIMIT_COOLDOWN` | Cooldown between requests in seconds (default: `5`) |

---

## Usage

Send any of the following to the bot:

- A **sticker** — returns a ZIP with all converted formats
- A **message containing custom emoji** — extracts and converts each emoji
- A **pack link** (`https://t.me/addstickers/...` or `https://t.me/addemoji/...`) — downloads and converts the entire pack

### Output Formats

| Format | Extension | Notes                                  |
| ------ | --------- | -------------------------------------- |
| TGS    | `.tgs`    | Original Telegram animated format      |
| JSON   | `.json`   | Uncompressed Lottie animation          |
| Lottie | `.lottie` | Compressed Lottie (LottieFiles format) |
| PNG    | `.png`    | First frame, 512×512 px                |

Non-TGS formats (WebM, WebP, MP4, GIF, etc.) are saved as-is without conversion.

---

## Docker

```bash
docker build -t emojisaverbot .

# First time — create the database file
touch /path/on/server/EmojiSaverBot.db

docker run -d --name emojisaverbot \
  --env-file .env \
  --restart unless-stopped \
  -v /path/on/server/EmojiSaverBot.db:/app/EmojiSaverBot.db \
  emojisaverbot
```

```bash
docker logs -f emojisaverbot       # live logs
docker restart emojisaverbot       # restart
docker stop emojisaverbot          # stop
docker rm emojisaverbot            # remove container
```

---

## License

This project is provided as-is for educational purposes.

---

<div align="center">

Made with ❤️ by [@bohd4nx](https://t.me/bohd4nx)

</div>
