"""Views for the authentication of the PassHunter web application."""
from urllib.parse import urlsplit

from flask import redirect, url_for, render_template, flash, request, Response
from flask_login import current_user, login_user, logout_user

from app.repository import account as account_repository
from app.web.auth import bp
from app.web.auth.forms import LoginForm, RegistrationForm


# The following login, logout, registration functions were heavily inspired by the function published on Miguel Grinberg's blog.
# Especially the redirects.
# Article name: The Flask Mega-Tutorial, Part V: Account Logins
# author: Miguel Grinberg
# created: 2023-12-03
# source: https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-v-user-logins [online]
# accessed: 2025-05-16


@bp.route('/login', methods=['GET', 'POST'])
def login() -> str | Response:
    """
    Login view. Log user in.

    Returns:
        str|Response: Rendered template for login or redirection to the next page
    """
    # Redirect the user to the home page if they are already authenticated.
    if current_user.is_authenticated:
        return redirect(url_for('index.index'))
    form = LoginForm()
    if form.validate_on_submit():
        # If an account is found and the password is correct, perform login and redirect to watchlists.
        account = account_repository.get_by_mail(form.email.data)
        if account and account_repository.check_password(account, form.password.data):
            login_user(account)
            # Perform redirect to the initially requested resource.
            # Relative paths are accepted, absolute paths are ignored.
            # Default redirect points to the home page.
            next_page = request.args.get('next')
            if not next_page or urlsplit(next_page).netloc != '':
                next_page = url_for('index.index')
            return redirect(next_page)
        # Else invalidate the login attempt
        flash('Invalid email or password.')
        return redirect(url_for('auth.login'))
    return render_template('auth/login.html', form=form)


@bp.route('/logout')
def logout() -> Response:
    """
    Logout view. Log user out.

    Returns:
        Response: Redirection to home page
    """
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('index.index'))


@bp.route('/register', methods=['GET', 'POST'])
def register() -> str | Response:
    """
    Register view.
    Register a new account.

    Returns:
        str|Response: Rendered template for register or redirection to login page
    """
    if current_user.is_authenticated:
        return redirect(url_for('index.index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        account = account_repository.create(form)
        flash(f'Account "{account.email}" has been now registered!')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', form=form)
