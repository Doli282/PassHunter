"""Repository layer - database access for the Monitor."""
from datetime import datetime
from typing import Any, Sequence

from sqlalchemy import select, create_engine, Row, RowMapping
from sqlalchemy.orm import Session

from models import db, Domain, Watchlist
from config import Config
from models.models import Alert

# Engine for connecting to the database.
engine = create_engine(Config.SQLALCHEMY_DATABASE_URI)

def get_monitored_domains() -> Sequence[Row[Any] | RowMapping | Any]:
    """Get all domains from the database that are in active watchlists."""
    statement = select(Domain).filter(Domain.watchlists.any(Watchlist.is_active==True))
    session = Session(engine)
    return session.scalars(statement).all()

def create_alert(created_at: datetime, domain: Domain, watchlist: Watchlist):
    """Create an alert for the given domain."""
    alert = Alert(is_new=True, domain=domain, created_at=created_at)
    alert.watchlist =
    db.session.add(alert)
    db.session.commit()
    return alert
