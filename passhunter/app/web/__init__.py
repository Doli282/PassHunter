"""Routes, views, and blueprints for the PassHunter web application."""
from flask_wtf import FlaskForm
from wtforms import SubmitField


class EmptyForm(FlaskForm):
    """
    Empty form with a universal submit button.

    Attributes:
        submit (SubmitField): The submit button.
    """
    submit = SubmitField('Submit')
