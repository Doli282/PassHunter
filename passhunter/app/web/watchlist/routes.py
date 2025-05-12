"""Views for the watchlist page of the PassHunter web application."""
from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from werkzeug import Response

import app.repository.domain as domain_repository
import app.repository.watchlist as watchlist_repository
from app.web import EmptyForm
from app.web.domain.forms import DomainForm
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


@bp.route('/watchlists/<int:watchlist_id>', methods=['GET', 'POST'])
@login_required
def view_watchlist(watchlist_id: int) -> str | Response:
    """
    View a specific watchlist belonging to the current user.

    Args:
        watchlist_id (int): The ID of the watchlist to view.
    Returns:
        str|Response: The 'watchlist view' template or redirection to the watchlist view.
    """
    watchlist = watchlist_repository.get_by_id(watchlist_id)
    page = request.args.get('page', 1, type=int)
    pagination = domain_repository.get_page_for_watchlist(watchlist_id, page)
    form = DomainForm()
    if form.validate_on_submit():
        domain_repository.upsert(form, watchlist)
        flash(f'Domain "{form.name.data}" added to watchlist "{watchlist.name}" successfully.', 'success')
        return redirect(url_for('watchlist.view_watchlist', watchlist_id=watchlist_id))
    return render_template('watchlist/view.html', watchlist=watchlist, form=form, pagination=pagination)


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
        watchlist = watchlist_repository.create(form, current_user)
        flash(f'Watchlist "{form.name.data}" created successfully.', 'success')
        return redirect(url_for('watchlist.view_watchlist', watchlist_id=watchlist.id))
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

@bp.route('/watchlists/<int:watchlist_id>/remove_domain/<int:domain_id>', methods=['GET', 'POST'])
@login_required
def remove_domain(watchlist_id: int, domain_id: int) -> str|Response:
    """
    Remove a domain from a watchlist for the current user.

    Args:
        watchlist_id (int): The ID of the watchlist to remove the domain from.
        domain_id (int): The ID of the domain to remove from the watchlist.
    Returns:
        str|Response: The 'watchlist remove domain' template or redirection to the watchlist view.
    """
    form = EmptyForm()
    watchlist = watchlist_repository.get_by_id(watchlist_id)
    domain = domain_repository.get_by_id(domain_id)
    if form.validate_on_submit():
        domain_repository.remove_domain_from_watchlist(domain, watchlist)
        flash(f'Domain "{domain.name}" removed from watchlist "{watchlist.name}" successfully.', 'success')
        return redirect(url_for('watchlist.view_watchlist', watchlist_id=watchlist_id))
    return render_template('watchlist/remove_domain.html', watchlist=watchlist, domain=domain, form=form)
