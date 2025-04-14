"""Models for the PassHunter web application. - Domains"""
from app.extensions import db

class Domain(db.Model):
    """Domain model for the PassHunter web application."""
    __tablename__ = 'domain'
    __table_args__ = {'comment': 'Monitored domains'}
    id = db.Column(db.Integer, primary_key=True, comment='Domain ID')
    name = db.Column(db.String(255), nullable=False, comment='Domain name')

    alerts = db.relationship('Alert', backref='domain', lazy=True, cascade='all, delete-orphan')
    watchlists = db.relationship('Watchlist', secondary='watchlist_domain_association', backref='domains', lazy=True)

    def __repr__(self):
        """Represent the Domain model as a string."""
        return f'<Domain {self.name}>'
