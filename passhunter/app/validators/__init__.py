"""Custom validators used in the PassHunter application"""
from flask_wtf import FlaskForm
from sqlalchemy import select
from wtforms.validators import ValidationError

from app import db

from models import Account


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
    account = db.session.scalar(select(Account).where(
        Account.email == email.data))
    if account is not None:
        raise ValidationError('Please use a different email address.')
