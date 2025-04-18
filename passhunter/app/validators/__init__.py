"""Custom validators used in the PassHunter application"""
from flask_wtf import FlaskForm
from sqlalchemy import select
from wtforms.validators import ValidationError

from app import db
from app.models.user import User


def validate_email(form: FlaskForm, email: str) -> None:
    """
    Validate that email address is not already registered.

    Arg:
        form (FlaskForm): Form to validate
        email (str): Email address to validate
    Returns:
         None
    Raises:
        ValidationError: If email is already registered
    """
    user = db.session.scalar(select(User).where(
        User.email == email.data))
    if user is not None:
        raise ValidationError('Please use a different email address.')
