# noinspection PyPackageRequirements
"""Telegram Downloader Daemon"""
import asyncio
import logging
import os.path
import re

from celery import Celery
from telethon import TelegramClient, events
from telethon.tl.custom import Message

from config import Config, ConfigCelery

# Set up logging.
logging.basicConfig(format=Config.LOGGING_FORMAT, level=os.getenv("LOGGING_LEVEL", "INFO"))

# Set up the Telegram client.
client = TelegramClient(session=Config.SESSION,api_id=int(Config.API_ID), api_hash=Config.API_HASH)

# Create queue for storing download requests.
queue = asyncio.Queue()

# Celery
celery = Celery('downloader')
celery.config_from_object(ConfigCelery)

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
    try:
        if message.document:
            logging.debug(f"{message.file.name} put in download queue.")
            await queue.put(message)
        else:
            logging.debug(f"Message id {message.id} does not contain documents.")
    except Exception as e:
        logging.error(f"Error while processing (putting into asyncio queue) message id {message.id}: {e}")

async def worker(name: str) -> None:
    """
    Worker function.
    Perform the actual download of a file.
    Take a message from the queue and perform the task.

    Args:
        name (str): Name of the worker.
    Returns:
        None
    """
    while True:
        filename = 'Unknown_File'
        try:
            # Get a message from the queue.
            message: Message = await queue.get()
            filename = message.file.name

            # Perform the actual download.
            await message.download_media(os.path.join(Config.DOWNLOAD_PATH, filename))
            logging.info(f"Worker '{name}' downloaded '{filename}'")

            # Extract a password from the message
            password =  extract_password(message.raw_text)

            # Send a task to celery.
            celery.send_task('extractor.extract_archive', args=[filename, password])
            logging.info(f"Worker '{name}' send '{filename}' to celery")
            # Notify the queue, the message has been processed.
            queue.task_done()
        except asyncio.CancelledError as e:
            logging.info(f"Worker '{name}' received cancel request")
            break
        except asyncio.TimeoutError as e:
            logging.error(f"Worker '{name}' reached timeout downloading '{filename}' with error: {e}")
        except Exception as e:
            logging.error(f"Worker '{name}' reached error while downloading '{filename}'. Error: {e}")

def extract_password(raw_text: str) -> str:
    """
    Extract password from text.

    Args:
        raw_text (str): Message possibly containing a password.

    Returns:
        Password or empty string if no password found.
    """
    match = re.search(r'[.\-]?\s*pass(word)?\s*[:=]\s*(\S+)', raw_text, re.IGNORECASE)
    if match:
        logging.debug(f"Password found in message")
        return match.group(2)
    else:
        logging.warning(f"No password found in message '{raw_text}'")
        return ""


# Start() function is based on the start() function implemented in a Downloader daemon made by alfem.
# author: Alfonso E.M. [alfem] (https://github.com/alfem)
# title: telegram-download-daemon
# medium: online
# version: commit 774025f
# year: 2023
# url: https://github.com/alfem/telegram-download-daemon/tree/master
# date: 2025-04-28
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
        logging.warning("Telegram client stopped!")


if __name__ == "__main__":
    """Start the Telegram Downloader Daemon"""
    with client.start(bot_token=Config.BOT_TOKEN):
        logging.info("Telegram daemon started.")
        client.loop.run_until_complete(start())