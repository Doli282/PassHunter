"""Configuration file for the Telegram Forwarder Daemon"""
import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))

load_dotenv(os.path.join(basedir, '.env'))

class Config(object):
    """Base configuration class"""
    # Telegram
    API_ID = os.getenv('TELEGRAM_API_ID')
    API_HASH = os.getenv('TELEGRAM_API_HASH')
    SESSION = 'forwarder_phone'
    # Logging
    LOGGING_FORMAT = '%(asctime)s Forwarder: %(levelname)s: %(message)s'
    # Application
    # IDs, usernames or links identifying the source channels
    SOURCE_CHANNEL_IDS = [-1002283692447, -1001935880746, -1002167657930, -1001828534036]
    # -1002494393489 ... test channel
    # -1002167657930 ... https://t.me/MavroCloud
    # -1001935880746 ... https://boxed.pw
    # -1001828534036... https://t.me/OBSERVERCLOUD2
    # ID, username or link identifying the target channel
    TARGET_CHANNEL_ID = -1002381035490
