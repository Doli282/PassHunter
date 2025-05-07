"""Alert Model"""
from datetime import datetime, timezone
from typing import TYPE_CHECKING

from . import db

if TYPE_CHECKING:
    from .domain import Domain
    from .watchlist import Watchlist


class Alert(db.Model):
    """Alert model for the PassHunter web application."""
    __tablename__ = 'alert'
    __table_args__ = {'comment': 'Alerts are raised for specific domains'}
    id: db.Mapped[int] = db.mapped_column(db.Integer, primary_key=True, comment='Alert ID')
    is_new: db.Mapped[bool] = db.mapped_column(db.Boolean, default=True, nullable=False, unique=False,
                                               comment='Whether the alert is new or not')
    created_at: db.Mapped[datetime] = db.mapped_column(db.DateTime, default=lambda: datetime.now(timezone.utc),
                                                       nullable=False, unique=False,
                                                       comment='Date and time the alert was created')
    domain_id: db.Mapped[int] = db.mapped_column(db.Integer, db.ForeignKey('domain.id', ondelete='CASCADE'), index=True,
                                                 nullable=False, unique=False,
                                                 comment='Domain ID for which the alert was raised')
    watchlist_id: db.Mapped[int] = db.mapped_column(db.Integer, db.ForeignKey('watchlist.id', ondelete='CASCADE'),
                                                    index=True, nullable=False, unique=False,
                                                    comment='Watchlist ID for which the alert was raised')

    domain: db.Mapped["Domain"] = db.relationship(back_populates='alerts', lazy=True)
    watchlist: db.Mapped["Watchlist"] = db.relationship(back_populates='alerts', lazy=True)

    def __repr__(self):
        """Represent the Alert model as a string."""
        return f'<Alert id={self.id}>'
