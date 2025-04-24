# Downloader - Telegram Daemon

This daemon downloads documents from new messages in a monitored channel.

## Installation

Make a virtual environment and install requirements from `requirements.txt`.
```shell
pip install -r requirements.txt
```

### Telegram Account
Register the Telegram application and obtain API ID on https://docs.telethon.dev/en/stable/basic/signing-in.html.
1. Login on https://my.telegram.org/.
2. Click API Development Tools.
3. Create a new application. Fill in the details.
4. Get API TOKEN and API HASH

Register a new bot by Telegram [@BotFather](https://t.me/botfather) and get the BOT TOKEN.

## Configuration

Daemon is configured through environment variables in `.env` file and configurable variables in `config.py`.

The `.env` file contains secrets for accessing Telegram API:
```dotenv
# Telegram variables
TELEGRAM_API_ID=...
TELEGRAM_API_HASH=...
BOT_TOKEN=...
```


## Usage

Run:
```shell
python3 downloader.py
```
