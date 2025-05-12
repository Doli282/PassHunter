"""Forms for the alert page of the PassHunter web application."""

from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField
from wtforms.validators import Optional, Length
from wtforms.fields import DateTimeLocalField

# Following code (class AlertFilterForm) was created by Cursor IDE.
# AI model: Claude 3.7 Sonnet
# Prompt: Create a filter form class for filtering alerts with fields for status, date range, domain name, and watchlist name
class AlertFilterForm(FlaskForm):
    """Form for filtering alerts."""
    status = SelectField('Status', 
                        choices=[('all', 'All'), ('new', 'New'), ('registered', 'Registered')],
                        default='new',
                        description='Filter by alert status')
    
    domain_name = StringField('Domain Name',
                            validators=[Optional(), Length(max=255)],
                            description='Filter by domain name (partial match)')
    
    watchlist_name = StringField('Watchlist Name',
                               validators=[Optional(), Length(max=255)],
                               description='Filter by watchlist name (partial match)')
    
    date_from = DateTimeLocalField('From Date',
                                   format='%Y-%m-%dT%H:%M',
                                   validators=[Optional()],
                                   description='Filter alerts from this date')
    
    date_to = DateTimeLocalField('To Date',
                                 format='%Y-%m-%dT%H:%M',
                                 validators=[Optional()],
                                 description='Filter alerts until this date')
    
    submit = SubmitField('Apply Filters')
    reset = SubmitField('Reset Filters') 