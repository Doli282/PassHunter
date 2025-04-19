"""Domain Model"""
from typing import Set, List, TYPE_CHECKING

from app.extensions import db
from app.models.watchlists_domains_association import watchlist_domain_association

if TYPE_CHECKING:
    from app.models import Watchlist
    from app.models.alert import Alert


class Domain(db.Model):
    """Domain model for the PassHunter web application."""
    __tablename__ = 'domain'
    __table_args__ = {'comment': 'Monitored domains'}
    id: db.Mapped[int] = db.mapped_column(db.Integer, primary_key=True, comment='Domain ID')
    name: db.Mapped[str] = db.mapped_column(db.String(255), nullable=False, unique=True, comment='Domain name')

    alerts: db.Mapped[List["Alert"]] = db.relationship(back_populates='domain', lazy=True,
                                                       cascade='delete, delete-orphan')
    watchlists: db.Mapped[Set["Watchlist"]] = db.relationship(secondary=watchlist_domain_association,
                                                              back_populates='domains', lazy=True)

    def __repr__(self):
        """Represent the Domain model as a string."""
        return f'<Domain id={self.id} name={self.name}>'
