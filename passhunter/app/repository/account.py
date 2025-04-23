"""Repository for Account"""
from sqlalchemy import select
from werkzeug.security import generate_password_hash, check_password_hash

from app import db, login
from app.models.account import Account
from app.web.auth.forms import RegistrationForm
from app.web.profile.forms import EditAccountForm


@login.user_loader
def get_by_id(account_id: int | str) -> Account | None:
    """
    Get an account by id.

    Args:
        account_id (int|str): Account id
    Returns:
        Account|None: Selected account or None if not found
    """
    return db.session.get(Account, int(account_id))


def get_by_id_404(account_id: int) -> Account:
    """
    Get an account by id. If none is found, raise 404 error.

    Args:
        account_id (int): Account id
    Raises:
        404: If the account is not found
    """
    return db.get_or_404(Account, ident=account_id)


def get_by_mail(email: str) -> Account | None:
    """
    Get an account by email.

    Args:
        email (str): Email address
    Returns:
        Account|None: Selected account or None if not found
    """
    statement = (select(Account).where(Account.email == email))
    return db.session.scalar(statement)


def create(form: RegistrationForm) -> Account:
    """
    Create a new account

    Args:
        form (RegistrationForm): Registration form
    Returns:
        Account: New account
    """
    account = Account()
    account.email = form.email.data
    account.name = form.name.data
    set_password(account, form.password.data)
    db.session.add(account)
    db.session.commit()
    return account


def update(account: Account, form: EditAccountForm) -> Account:
    """
    Edit an account

    Args:
        account (Account): Account to be updated
        form (EditAccountForm): Edit account form
    Returns:
        Account: Updated account
    """
    account.name = form.name.data
    db.session.add(account)
    db.session.commit()
    return account


def delete(account: Account) -> None:
    """
    Delete an account.
    Hard delete is performed.

    Args:
        account (Account): Account to be deleted
    Returns:
        None
    """
    db.session.delete(account)
    db.session.commit()


def set_password(account: Account, password: str) -> Account:
    """
    Set the password for an account as a hashed password

    Args:
        account (Account): Account to be updated
        password (str): New password in plain text
    Returns:
        Account: Updated account
    """
    account.password_hash = generate_password_hash(password)
    return account


def check_password(account: Account, password: str) -> bool:
    """
    Check if password matches account's password

    Args:
        account (Account): Account to be checked
        password (str): Provided password in plain text
    Returns:
        bool: True if password matches, False otherwise
    """
    return check_password_hash(account.password_hash, password)
