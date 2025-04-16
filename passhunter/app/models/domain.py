"""Models for the PassHunter web application. - Domains"""
from app.extensions import db
from app.models.watchlists_domains_association import watchlist_domain_association

class Domain(db.Model):
    """Domain model for the PassHunter web application."""
    __tablename__ = 'domain'
    __table_args__ = {'comment': 'Monitored domains'}
    id = db.Column(db.Integer, primary_key=True, comment='Domain ID')
    name = db.Column(db.String(255), nullable=False, comment='Domain name')

    alerts = db.relationship('Alert', back_populates='domain', lazy=True, cascade='all, delete-orphan')
    watchlists = db.relationship('Watchlist', secondary=watchlist_domain_association, back_populates='domains', lazy=True)

    def __repr__(self):
        """Represent the Domain model as a string."""
        return f'<Domain {self.name}>'
