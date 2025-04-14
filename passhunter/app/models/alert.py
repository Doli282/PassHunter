"""Models for the PassHunter web application. - Alerts"""
from app.extensions import db
from datetime import datetime, timezone

class Alert(db.Model):
    """Alert model for the PassHunter web application."""
    __tablename__ = 'alert'
    __table_args__ = {'comment': 'Alerts are raised for specific domains'}
    id = db.Column(db.Integer, primary_key=True, comment='Alert ID')
    is_new = db.Column(db.Boolean, default=True, comment='Whether the alert is new or not')
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), comment='Date and time the alert was created')
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), comment='Date and time the alert was updated')
    domain_id = db.Column(db.Integer, db.ForeignKey('domain.id', ondelete='CASCADE'), index=True, nullable=False, comment='Domain ID for which the alert was raised')

    domain = db.relationship('Domain', backref=db.backref('alerts', lazy=True))

    def __repr__(self):
        """Represent the Alert model as a string."""
        return f'<Alert {self.id}>'