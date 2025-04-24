# Forwarder - Telegram Daemon

## Configuration

Daemon is configured through environment variables in `.env` file and configurable variables in `config.py`.

The `.env` file contains secrets for accessing Telegram API:
```dotenv
# Telegram variables
TELEGRAM_API_ID=...
TELEGRAM_API_HASH=...
```

The `config.py` 