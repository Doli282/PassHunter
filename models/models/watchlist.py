"""Watchlist model"""
from typing import Optional, Set, List, TYPE_CHECKING

from . import db
from .watchlists_domains_association import watchlist_domain_association

if TYPE_CHECKING:
    from .alert import Alert
    from .domain import Domain
    from .account import Account


class Watchlist(db.Model):
    """Watchlist model for the PassHunter web application."""
    __tablename__ = 'watchlist'
    __table_args__ = {'comment': 'Watchlists are used to group monitored domains'}
    id: db.Mapped[int] = db.mapped_column(db.Integer, primary_key=True, comment='Watchlist ID')
    account_id: db.Mapped[int] = db.mapped_column(db.Integer, db.ForeignKey('account.id'), nullable=False,
                                                  comment='Account ID')
    name: db.Mapped[str] = db.mapped_column(db.String(255), nullable=False, unique=True, comment='Watchlist name')
    description: db.Mapped[Optional[str]] = db.mapped_column(db.Text, nullable=True, unique=False,
                                                             comment='Watchlist description')
    is_active: db.Mapped[bool] = db.mapped_column(db.Boolean, default=True, nullable=False, unique=False,
                                                  comment='Whether the watchlist is active or not')
    email: db.Mapped[Optional[str]] = db.mapped_column(db.String(255), nullable=True, unique=False,
                                                       comment='Email address to send alerts to')
    send_alerts: db.Mapped[bool] = db.mapped_column(db.Boolean, default=True, nullable=False, unique=False,
                                                    comment='Whether to send email alerts for this watchlist')

    account: db.Mapped["Account"] = db.relationship(back_populates='watchlists', lazy=True)
    domains: db.Mapped[Set["Domain"]] = db.relationship(secondary=watchlist_domain_association,
                                                        back_populates='watchlists', lazy=True)
    alerts: db.Mapped[List["Alert"]] = db.relationship(back_populates='watchlist', lazy=True,
                                                       cascade='delete, delete-orphan')

    def __repr__(self):
        """Represent the Watchlist model as a string."""
        return f'<Watchlist id={self.id} name={self.name}>'

    def print_active(self) -> str:
        """Return the active status of the watchlist."""
        return 'Active' if self.is_active else 'Inactive'

    def print_send_alerts(self) -> str:
        """Return the 'send alerts' status of the watchlist."""
        return 'Enabled' if self.send_alerts else 'Disabled'