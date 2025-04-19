"""Models for the PassHunter web application."""
# from sqlalchemy_utils import auto_delete_orphans

from app.models.account import Account
from app.models.alert import Alert
from app.models.domain import Domain
from app.models.watchlist import Watchlist

# Auto delete orphaned domains
# auto_delete_orphans(Watchlist.domains)
