"""Views for the watchlist page of the PassHunter web application."""
from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from werkzeug import Response

import app.repository.watchlist as watchlist_repository
from app.web import EmptyForm
from app.web.watchlist import bp
from app.web.watchlist.forms import WatchlistForm


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


@bp.route('/watchlists/<int:watchlist_id>')
@login_required
def view_watchlist(watchlist_id: int) -> str:
    """
    View a specific watchlist belonging to the current user.

    Args:
        watchlist_id (int): The ID of the watchlist to view.
    Returns:
        str: The watchlist view template.
    """
    watchlist = watchlist_repository.get_by_id(watchlist_id)
    return render_template('watchlist/view.html', watchlist=watchlist)


@bp.route('/watchlists/create', methods=['GET', 'POST'])
@login_required
def create_watchlist() -> str | Response:
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
    return render_template('watchlist/upsert.html', form=form)


@bp.route('/watchlists/<int:watchlist_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_watchlist(watchlist_id: int) -> str|Response:
    """
    Edit an existing watchlist for the current user.

    Args:
        watchlist_id (int): The ID of the watchlist to edit.
    Returns:
        str|Response: The 'watchlist edit' template or redirection to the watchlist view.
    """
    watchlist = watchlist_repository.get_by_id(watchlist_id)
    form = WatchlistForm(obj=watchlist)
    if form.validate_on_submit():
        watchlist_repository.update(form, watchlist)
        flash(f'Watchlist "{form.name.data}" updated successfully.', 'success')
        return redirect(url_for('watchlist.view_watchlist', watchlist_id=watchlist_id))
    return render_template('watchlist/upsert.html', form=form, watchlist=watchlist)


@bp.route('/watchlists/<int:watchlist_id>/delete', methods=['GET', 'POST'])
@login_required
def delete_watchlist(watchlist_id: int) -> str|Response:
    """
    Delete an existing watchlist for the current user.

    Args:
        watchlist_id (int): The ID of the watchlist to delete.
    Returns:
        str|Response: The 'watchlist delete' template or redirection to the watchlist list.
    """
    watchlist = watchlist_repository.get_by_id(watchlist_id)
    form = EmptyForm()
    if form.validate_on_submit():
        watchlist_repository.delete_by_id(watchlist_id)
        flash(f'Watchlist "{watchlist.name}" deleted successfully.', 'success')
        return redirect(url_for('watchlist.list_watchlists'))
    return render_template('watchlist/delete.html', watchlist=watchlist, form=form)

