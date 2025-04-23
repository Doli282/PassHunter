"""Forms for the watchlist page of the PassHunter web application."""
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, BooleanField
from wtforms.fields.simple import EmailField
from wtforms.validators import DataRequired, Email, Optional, Length


class WatchlistForm(FlaskForm):
    """Form for creating and editing watchlists."""
    name = StringField('Name', validators=[DataRequired(message='This field must not be empty.'), Length(max=255,
                                                                                                         message='The maximal length of accepted input is 255 characters.')],
                       description='Name of your watchlist')
    description = TextAreaField('Description', validators=[Optional()],
                                description='Meaningful description of the watchlist.')
    is_active = BooleanField('Active', default=True,
                             description='Whether the watchlist is active or not. Deactivated watchlists are not monitored.')
    email = EmailField('Email', validators=[Optional(), Length(max=255,
                                                               message='The maximal length of accepted input is 255 characters.'),
                                            Email(message='Input must adhere to email structure.')],
                       description='Email address to send alerts to.')
    send_alerts = BooleanField('Mail Alerts', default=True,
                               description='Whether to send email alerts for this watchlist.')
    submit = SubmitField('Save')
