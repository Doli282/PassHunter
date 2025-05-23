# Forwarder - Telegram Daemon

This daemon forwards messages that contain documents to the specified channel.

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

#### Authentication

During the first lunch an authentication is required when a BOT TOKEN was not provided.
Later a `XX.session` file is created and used for repeated login.
Authentication with a phone number and a code must be manual.
The authentication code is sent during verification to another device (to a phone or another client).

#### BOT vs. Phone

When using a BOT TOKEN it can forward messages only from channels where the bot is a member.
When using a phone number, it can forward from any channels defined in the list.

## Configuration

Daemon is configured through environment variables in `.env` file and configurable variables in `config.py`.

The `.env` file contains secrets for accessing Telegram API:
```dotenv
# Telegram variables
TELEGRAM_API_ID=...
TELEGRAM_API_HASH=...
```

The `config.py` file contains configuration.
Pay extra attention to the definitions of source and target channels:
```python
# IDs, usernames or links identifying the source channels
SOURCE_CHANNEL_IDS = [-1002283692447, -1002494393489, -1001935880746]
# ID, username or link identifying the target channel
TARGET_CHANNEL_ID = -1002381035490
```
Change the values for IDs of channels intended as a source, or as a target.


## Usage

Run:
```shell
python3 forwarder.py
```

## Testing

Test scenarios are described in the /test/ directory.

To launch the automated test, run the following command from the module root directory:
```shell
python3 -m unittest tests/test_forward.py
```
