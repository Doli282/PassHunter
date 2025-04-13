"""Models for the PassHunter web application. - Alerts"""
from app.extensions import db
from datetime import datetime

class Alert(db.Model):
    """Alert model for the PassHunter web application."""
    __tablename__ = 'alerts'
    __table_args__ = {'comment': 'Alerts are raised for specific domains'}
    id = db.Column(db.Integer, primary_key=True, comment='Alert ID')
    is_new = db.Column(db.Boolean, default=True, comment='Whether the alert is new or not')
    created_at = db.Column(db.DateTime, default=datetime.now, comment='Date and time the alert was created')
    updated_at = db.Column(db.DateTime, default=datetime.now, comment='Date and time the alert was updated')
    domain_id = db.Column(db.Integer, db.ForeignKey('domains.id', ondelete='CASCADE'), nullable=False, comment='Domain ID for which the alert was raised')

    domain = db.relationship('Domain', backref=db.backref('alerts', lazy=True))