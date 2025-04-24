"""Telegram Downloader Daemon"""
import asyncio
import logging
import os.path

from telethon import TelegramClient, events
from telethon.tl.custom import Message

from config import Config

# Set up logging.
logging.basicConfig(format=Config.LOGGING_FORMAT, level=logging.INFO)

# Set up the Telegram client.
client = TelegramClient(session=Config.SESSION,api_id=int(Config.API_ID), api_hash=Config.API_HASH)

# Create queue for storing download requests.
queue = asyncio.Queue()

@client.on(events.NewMessage(incoming=True))
async def handler(message: Message) -> None:
    """
    Define handler for incoming messages.
    Monitors only specified channels
    Check for downloadable documents.

    Args:
        message (Message): The incoming Telegram message object containing message data and metadata.
    Returns:
        None
    """
    logging.info(f"Processing message id {message.id}")
    # If the message contains a document, put it in a queue for further processing.
    if message.document:
        logging.info(f"{message.file.name} put in download queue.")
        await queue.put(message)
    else:
        logging.info(f"Message id {message.id} does not contain documents.")


async def worker(name: str) -> None:
    while True:
        filename = 'Unknown_File'
        try:
            # Get a message from the queue.
            message: Message = await queue.get()
            filename = message.file.name

            # Perform the actual download.
            await message.download_media(os.path.join(Config.DOWNLOAD_PATH, filename))
            # Notify the queue, the message has been processed.
            queue.task_done()
        except asyncio.TimeoutError as e:
            logging.error(f"Worker '{name}' reached timeout downloading '{filename}' with error: {e}")
        except Exception as e:
            logging.error(f"Worker '{name}' reached error while downloading '{filename}'. Error: {e}")


async def start() -> None:
    """
    Starting function for the Telegram client.
    Start workers and launch the application.

    Returns:
        None
    """
    # List of tasks for parallel processing by workers.
    tasks = []
    try:
        # Create workers.
        loop = asyncio.get_event_loop()
        for i in range(Config.WORKER_COUNT):
            task = loop.create_task(worker(f"Worker-{i}"))
            tasks.append(task)
        # Run the client until Ctrl+C is pressed, or the client disconnects
        logging.debug("Workers started.")
        await client.run_until_disconnected()
        logging.warning("Interrupt caught. Disconnecting the client...")
    finally:
        # Cancel worker tasks.
        for task in tasks:
            task.cancel()
        # Wait until all worker tasks are canceled.
        await asyncio.gather(*tasks, return_exceptions=True)
        logging.debug("Workers stopped.")
        # Stop the client.
        client.disconnect()
        logging.info("Telegram client stopped!")


if __name__ == "__main__":
    """Start the Telegram Downloader Daemon"""
    with client.start(bot_token=Config.BOT_TOKEN):
        logging.info("Telegram daemon started.")
        client.loop.run_until_complete(start())