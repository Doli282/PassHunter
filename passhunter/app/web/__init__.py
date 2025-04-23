"""Routes, views, and blueprints for the PassHunter web application."""
from flask_wtf import FlaskForm
from wtforms import SubmitField


class EmptyForm(FlaskForm):
    """
    Empty form with a delete submit button.

    Attributes:
        submit (SubmitField): The submit button (value='delete').
    """
    submit = SubmitField('Delete')
