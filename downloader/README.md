# Downloader - Telegram Daemon

This daemon downloads documents from new messages in a monitored channel.

## Installation

Make a virtual environment and install requirements from `requirements.txt`.
```shell
pip install -r requirements.txt
```

`If libssl is available on your system, the library will make use of it to speed up some critical parts such as encrypting and decrypting the messages. Files will notably be sent and downloaded faster.'
source: https://docs.telethon.dev/en/stable/developing/philosophy.html

### Telegram Account
Register the Telegram application and obtain API ID. Based on https://docs.telethon.dev/en/stable/basic/signing-in.html.
1. Login on https://my.telegram.org/.
2. Click API Development Tools.
3. Create a new application. Fill in the details.
4. Get API TOKEN and API HASH.

Register a new bot by Telegram [@BotFather](https://t.me/botfather) and get the BOT TOKEN.

The telegram service may want an authentication during the first launch when a BOT TOKEN was not provided.
Then a `XXX.session` is created and used. 
However, better results were observed with the use of a BOT TOKEN.

Add the bot to the channel from which it should download files.

## Configuration

Daemon is configured through environment variables in `.env` file and configurable variables in `config.py`.

The `.env` file contains secrets for accessing Telegram API:
```dotenv
# Telegram variables
TELEGRAM_API_ID=...
TELEGRAM_API_HASH=...
BOT_TOKEN=...

# RabbitMQ
CELERY_BROKER_URL=...
```

## Usage

Run:
```shell
python3 downloader.py
```

## Tests

Tests scenarios are described in the /tests/ directory.
To launch the automated test, run the following command from the module root directory:
```shell
python3 -m unittest tests/test_downloader.py
```

