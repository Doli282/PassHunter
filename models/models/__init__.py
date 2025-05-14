"""Models for the PassHunter web application."""
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from .account import Account
from .alert import Alert
from .domain import Domain
from .file import File
from .watchlist import Watchlist
