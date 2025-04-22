"""Views for the watchlist page of the PassHunter web application."""
from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from werkzeug import Response

import app.repository.watchlist as watchlist_repository
from app.extensions import db
from app.models.alert import Alert
from app.models.domain import Domain
from app.models.watchlist import Watchlist
from app.web.watchlist import bp
from app.web.watchlist.forms import (
    WatchlistForm,
    DeleteWatchlistForm,
    AddDomainForm,
    RemoveDomainForm
)


@bp.route('/watchlists')
@login_required
def list_watchlists() -> str:
    """
    List all watchlists belonging to the current user in pages.

    Returns:
        str: The watchlist list template.
    """
    page = request.args.get('page', 1, type=int)
    pagination = watchlist_repository.get_page(page)
    return render_template(
        'watchlist/list.html',
        pagination=pagination
    )

# TODO view one watchlist


@bp.route('/watchlists/create', methods=['GET', 'POST'])
@login_required
def create() -> str|Response:
    """
    Create a new watchlist for the current user.

    Returns:
        str|Response: The 'watchlist create' template or redirection to the watchlist list.
    """
    form = WatchlistForm()
    if form.validate_on_submit():
        watchlist_repository.create(form, current_user)
        flash(f'Watchlist "{form.name.data}" created successfully.', 'success')
        return redirect(url_for('watchlist.list_watchlists'))
    return render_template('watchlist/create.html', form=form)
