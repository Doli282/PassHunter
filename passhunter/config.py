"""Configuration for the PassHunter web application."""
from dotenv import load_dotenv
import os

basedir = os.path.abspath(os.path.dirname(__file__))

load_dotenv(os.path.join(basedir, '.env'))

class Config(object):
    """Base configuration class."""
    SECRET_KEY = os.getenv('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    PER_PAGE = 5
    MAIL_SERVER = os.getenv('MAIL_SERVER')
    MAIL_PORT = int(os.getenv('MAIL_PORT') or 25)
    MAIL_USE_TLS = os.getenv('MAIL_USE_TLS') is not None
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    ADMINS = ['DolanskyL@email.cz']
    LOGGING_DIR = 'logs'
    LOGGING_FILE = 'passhunter.log'