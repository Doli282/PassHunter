"""Telegram Forwarder Daemon - forwarding messages between channels"""
import logging

from telethon import TelegramClient, events
from telethon.tl.custom import Message

from config import Config

# Set up logging.
logging.basicConfig(format=Config.LOGGING_FORMAT, level=logging.INFO)

# Set up the Telegram client.
client = TelegramClient(session=Config.SESSION,api_id=int(Config.API_ID), api_hash=Config.API_HASH)

@client.on(events.NewMessage(chats=Config.SOURCE_CHANNEL_IDS))
async def forward(message: Message) -> None:
    """
    Forward messages from monitored channels.
    Forwards only messages with documents.

    Args:
        message (Message): Message to forward.
    Returns:
        None
    """
    try:
        if message.document:
            await message.forward_to(int(Config.TARGET_CHANNEL_ID))
            logging.info(f"Forwarded message from {message.to_id} with '{message.file.name}'.")
    except Exception as e:
        logging.error(f"Unable to forward message due to error: {str(e)}")

if __name__ == "__main__":
    """Start the Telegram Forwarder Daemon."""
    with client.start():
        logging.info("Telegram daemon started.")
        client.run_until_disconnected()
        logging.warning("Telegram daemon stopped.")