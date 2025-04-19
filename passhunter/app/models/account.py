"""Account model"""
from typing import Optional, List
from typing import TYPE_CHECKING

from flask_login import UserMixin

from app.extensions import db

if TYPE_CHECKING:
    from app.models import Watchlist


class Account(db.Model, UserMixin):
    """Account model for the PassHunter web application."""
    __tablename__ = 'account'
    __table_args__ = {'comment': 'Registered accounts'}
    id: db.Mapped[int] = db.mapped_column(db.Integer, primary_key=True, comment='Account ID')
    email: db.Mapped[str] = db.mapped_column(db.String(256), nullable=False, unique=True, index=True,
                                             comment='Email address for the account')
    name: db.Mapped[Optional[str]] = db.mapped_column(db.String(256), nullable=True, unique=False,
                                                      comment="Account's name")
    password_hash: db.Mapped[str] = db.mapped_column(db.String(256), nullable=False, unique=False,
                                                     comment='Password hash')

    watchlists: db.Mapped[List["Watchlist"]] = db.relationship('Watchlist', back_populates='account', lazy=True,
                                                               cascade='all, delete-orphan')

    def __repr__(self):
        """Represent the Account model as a string"""
        return f'<Account id={self.id} email={self.email}>'

    def account_info(self):
        """
        Return the account information

        Returns:
            dict: Account information
        """
        return {
            'email': self.email,
            'name': self.name,
        }
