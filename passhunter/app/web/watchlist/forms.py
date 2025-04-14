"""Forms for the watchlist page of the PassHunter web application."""
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, BooleanField
from wtforms.validators import DataRequired, Email, Optional


class WatchlistForm(FlaskForm):
    """Form for creating and editing watchlists."""
    name = StringField('Name', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[Optional()])
    is_active = BooleanField('Active', default=True, description='Whether the watchlist is active or not. Deactivated watchlists are not monitored.')
    mail_address = StringField('Email', validators=[Optional(), Email()], description='Email address to send alerts to.')
    mail_alerts = BooleanField('Mail Alerts', default=True, description='Whether to send email alerts for this watchlist.')
    submit = SubmitField('Save')

class DeleteWatchlistForm(FlaskForm):
    """Form for deleting a watchlist."""
    submit = SubmitField('Delete')

class AddDomainForm(FlaskForm):
    """Form for adding a domain to a watchlist."""
    domain = StringField('Domain', validators=[DataRequired()])
    submit = SubmitField('Add Domain')

class RemoveDomainForm(FlaskForm):
    """Form for removing a domain from a watchlist."""
    submit = SubmitField('Remove Domain')
