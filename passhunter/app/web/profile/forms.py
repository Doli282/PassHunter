"""Forms for the profile page of the PassHunter web application."""
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import Length, Optional


class EditAccountForm(FlaskForm):
    """Form for editing the user's profile."""
    name = StringField('Name', validators=[Optional(), Length(min=0, max=255, message='The maximal length of accepted input is 255 characters.')])
    submit = SubmitField('Save')