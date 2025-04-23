"""Forms for the domain page of the PassHunter web application."""
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length


class DomainForm(FlaskForm):
    """Form for adding domains to a watchlist."""
    name = StringField('Domain', validators=[DataRequired(message='This field must not be empty.'), Length(max=255,
                                                                                                         message='The maximal length of accepted input is 255 characters.')],
                         description='Domain to add to your watchlist.')
    submit = SubmitField('Add')
