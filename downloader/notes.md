## Installation
```shell
pip -m venv venv-telegram
source venv-telegram/bin/activate

pip install --upgrade pip
pip install telethon
pip install python-dotenv

# For better performance during file download as mentioned in https://docs.telethon.dev/en/stable/basic/installation.html
pip install cryptg
```

```shell
pip freeze > requirements.txt
pip install -r requirements.txt
```

`If libssl is available on your system, the library will make use of it to speed up some critical parts such as encrypting and decrypting the messages. Files will notably be sent and downloaded faster.'
source: https://docs.telethon.dev/en/stable/developing/philosophy.html

## Telegram Account
Register the Telegram application and obtain API ID on https://docs.telethon.dev/en/stable/basic/signing-in.html.
1. Login on https://my.telegram.org/.
2. Click API Development Tools.
3. Create a new application. Fill in the details.

## Bot vs. Phone vs. Admin rights? 

When BOT_TOKEN is not provided, the client asks for a phone number and code for verification.
With the bot_token, it monitors only channels where the bot is added.
A bot can be added to a channel only as an admin.
For downloading files, one needs admin rights.

Tried without bot token:
- asked for phone number
- did not download file from any channel
