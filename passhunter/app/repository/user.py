"""Repository for User"""
from sqlalchemy import select
from werkzeug.security import generate_password_hash, check_password_hash

from app import db, login
from app.models.user import User
from app.web.auth.forms import RegistrationForm


@login.user_loader
def get_by_id(user_id: int | str) -> User | None:
    """
    Get user by id.

    Args:
        user_id (int|str): User id
    Returns:
        User|None: Selected user or None if not found
    """
    return db.session.get(User, int(user_id))


def get_by_mail(email: str) -> User | None:
    """
    Get user by email.

    Args:
        email (str): Email address
    Returns:
        User|None: Selected user or None if not found
    """
    statement = (select(User).where(User.email == email))
    return db.session.scalar(statement)


def create(form: RegistrationForm) -> User:
    """
    Create a new user

    Args:
        form (RegistrationForm): Registration form
    Returns:
        User: New user
    """
    user = User()
    user.email = form.email.data,
    user.name = form.name.data
    set_password(user, form.password.data)
    db.session.add(user)
    db.session.commit()
    return user


# TODO update
# TODO delete

def set_password(user: User, password: str) -> User:
    """
    Set password for user as a hashed password

    Args:
        user (User): User to be updated
        password (str): New password in plain text
    Returns:
        User: Updated user
    """
    user.password_hash = generate_password_hash(password)
    return user


def check_password(user: User, password: str) -> bool:
    """
    Check if password matches user's password

    Args:
        user (User): User to be checked
        password (str): Provided password in plain text
    Returns:
        bool: True if password matches, False otherwise
    """
    return check_password_hash(user.password_hash, password)
