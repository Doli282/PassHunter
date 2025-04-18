"""User model"""
from typing import Optional, List
from typing import TYPE_CHECKING

from flask_login import UserMixin

from app.extensions import db

if TYPE_CHECKING:
    from app.models import Watchlist


class User(db.Model, UserMixin):
    """User model for the PassHunter web application."""
    __tablename__ = 'user'
    __table_args__ = {'comment': 'Registered users'}
    id: db.Mapped[int] = db.mapped_column(db.Integer, primary_key=True, comment='User ID')
    email: db.Mapped[str] = db.mapped_column(db.String(256), nullable=False, unique=True, index=True,
                                             comment='Email address of the user')
    name: db.Mapped[Optional[str]] = db.mapped_column(db.String(256), nullable=True, unique=False,
                                                      comment="User's name")
    password_hash: db.Mapped[str] = db.mapped_column(db.String(256), nullable=False, unique=False,
                                                     comment='Password hash')

    watchlists: db.Mapped[List["Watchlist"]] = db.relationship('Watchlist', back_populates='user', lazy=True,
                                                               cascade='all, delete-orphan')

    def __repr__(self):
        """Represent the User model as a string"""
        return f'<User id={self.id} email={self.email}>'
