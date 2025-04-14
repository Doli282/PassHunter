"""Models for the PassHunter web application. - Watchlists"""
from app.extensions import db

class Watchlist(db.Model):
    """Watchlist model for the PassHunter web application."""
    __tablename__ = 'watchlist'
    __table_args__ = {'comment': 'Watchlists are used to monitor domains'}
    id = db.Column(db.Integer, primary_key=True, comment='Watchlist ID')
    name = db.Column(db.String(255), nullable=False, unique=True, comment='Watchlist name')
    description = db.Column(db.Text, nullable=True, comment='Watchlist description')
    is_active = db.Column(db.Boolean, default=True, comment='Whether the watchlist is active or not')
    mail_address = db.Column(db.String(255), nullable=True, comment='Email address to send alerts to')
    mail_alerts = db.Column(db.Boolean, default=True, comment='Whether to send email alerts for this watchlist')

    domains = db.relationship('Domain', secondary='watchlist_domain_association', backref='watchlists', lazy=True)

    def __repr__(self):
        """Represent the Watchlist model as a string."""
        return f'<Watchlist {self.name}>'
