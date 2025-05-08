"""Models for the PassHunter web application."""
from flask_sqlalchemy import SQLAlchemy

# from sqlalchemy_utils import auto_delete_orphans

db = SQLAlchemy()

from .account import Account
from .alert import Alert
from .domain import Domain
from .file import File
from .watchlist import Watchlist

# Auto delete orphaned domains
# auto_delete_orphans(Watchlist.domains)
