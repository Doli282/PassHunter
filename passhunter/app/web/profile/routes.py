"""Views for the profile page of the PassHunter web application."""
from flask import render_template, flash, redirect, url_for, Response, request
from flask_login import login_required, current_user, logout_user

from app.repository import account as account_repository
from app.web import EmptyForm
from app.web.profile import bp
from app.web.profile.forms import EditAccountForm


@bp.route('/profile')
@login_required
def profile() -> str:
    """
    Render the profile page.

    Returns:
        str: The rendered profile page.
    """
    return render_template('profile/profile.html')

@bp.route('/profile/edit', methods=['GET', 'POST'])
@login_required
def edit() -> str|Response:
    """
    Edit the user's account information.

    Returns:
        str|Response: The rendered edit page or a redirect to the profile page.
    """
    form = EditAccountForm(obj=current_user)
    if form.validate_on_submit():
        account_repository.update(current_user, form)
        flash('Your changes have been saved.')
        return redirect(url_for('profile.profile'))
    return render_template('profile/edit.html', form=form)


@bp.route('/profile/delete', methods=['GET', 'POST'])
@login_required
def delete() -> str|Response:
    """
    Delete the user's account.

    Returns:
        str|Response: The rendered delete page or a redirect to the index page.
    """
    form = EmptyForm()
    if form.validate_on_submit():
        account_repository.delete(current_user)
        flash('Your account has been deleted.')
        return redirect(url_for('index.index'))
    return render_template('profile/delete.html', form=form)
