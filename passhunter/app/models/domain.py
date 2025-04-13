"""Models for the PassHunter web application. - Domains"""
from app.extensions import db

class Domain(db.Model):
    """Domain model for the PassHunter web application."""
    __tablename__ = 'domains'
    __table_args__ = {'comment': 'Monitored domains'}
    id = db.Column(db.Integer, primary_key=True, comment='Domain ID')
    name = db.Column(db.String(255), nullable=False, unique=True, comment='Domain name')

    alerts = db.relationship('Alert', backref='domain', lazy=True, cascade='all, delete-orphan')
    watchlists = db.relationship('Watchlist', secondary='watchlists_domains_association', backref='domains', lazy=True)
