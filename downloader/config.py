"""Configuration file for the Telegram Downloader Daemon"""
import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))

load_dotenv(os.path.join(basedir, '.env'))

class Config(object):
    """Base configuration class"""
    # Telegram
    API_ID = os.getenv('TELEGRAM_API_ID')
    API_HASH = os.getenv('TELEGRAM_API_HASH')
    BOT_TOKEN = os.getenv('BOT_TOKEN')
    SESSION = 'downloader'
    # Logging
    LOGGING_FORMAT = '%(asctime)s Downloader: %(levelname)s: %(message)s'
    # Application
    WORKER_COUNT = 4
    DOWNLOAD_PATH = '/tmp'
