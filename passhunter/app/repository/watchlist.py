"""Repository for Watchlist"""
from typing import List, Dict, Any, Tuple

from flask import current_app
from flask_sqlalchemy.pagination import Pagination
from sqlalchemy import func, select

from app import db
from app.models import Account
from app.models.alert import Alert
from app.models.watchlist import Watchlist
from app.web.watchlist.forms import WatchlistForm


def get_all() -> List[Watchlist]:
    """
    Retrieve all Watchlists.

    Returns:
        List[Watchlist]: List of all Watchlists.
    """
    query = db.select(Watchlist)
    return db.session.scalars(query).all()


def get_page(page: int = 1) -> Pagination:
    """
    Retrieve paginated Watchlists.

    Args:
        page (int): Page number.
    Returns:
        Pagination: Paginated Watchlists.
    """
    query = db.select(Watchlist)
    return db.paginate(select=query, page=page, max_per_page=current_app.config['WATCHLISTS_PER_PAGE'])


def get_by_id(watchlist_id: int) -> Watchlist:
    """
    Retrieve Watchlist by ID.

    Args:
        watchlist_id (int): Watchlist ID.
    Returns:
        Watchlist: Watchlist by ID.
    """
    return db.get_or_404(Watchlist, id=watchlist_id)


def create(form: WatchlistForm, user: Account) -> Watchlist:
    """
    Create a new Watchlist.

    Args:
        form (WatchlistForm): Watchlist form.
        user (Account): Account - owner of the Watchlist.
    Returns:
        Watchlist: New Watchlist.
    """
    watchlist = Watchlist()
    form.populate_obj(watchlist)
    watchlist.account = user
    db.session.add(watchlist)
    db.session.commit()
    return watchlist


def update(watchlist: Watchlist, form: WatchlistForm) -> Watchlist:
    """
    Update an existing Watchlist.

    Args:
        watchlist (Watchlist): Watchlist to update.
        form (WatchlistForm): Watchlist form.
    Returns:
        Watchlist: Updated Watchlist.
    """
    form.populate_obj(watchlist)
    db.session.commit()
    return watchlist


def delete_by_id(watchlist_id: int) -> Watchlist:
    """
    Delete Watchlist by ID.

    Args:
        watchlist_id (int): Watchlist ID.
    Returns:
        Watchlist: Deleted Watchlist.
    """
    watchlist = get_by_id(watchlist_id)
    db.session.delete(watchlist)
    db.session.commit()
    return watchlist


def get_by_account_id_with_stats(account_id: int, page: int = 1) -> Tuple[Pagination, Dict[int, Dict[str, Any]]]:
    """
    Retrieve paginated Watchlists for a specific account with alert statistics.

    Args:
        account_id (int): Account ID.
        page (int): Page number.
    Returns:
        Tuple[Pagination, Dict[int, Dict[str, Any]]]: Paginated Watchlists and a dictionary with alert stats.
    """
    # Get paginated watchlists for the account
    query = db.select(Watchlist).filter(Watchlist.account_id == account_id)
    watchlists_pagination = db.paginate(select=query, page=page, max_per_page=current_app.config['WATCHLISTS_PER_PAGE'])

    # Get watchlist IDs from the current page
    watchlist_ids = [w.id for w in watchlists_pagination.items]

    # Initialize stats dictionary with default values for all watchlists
    stats = {watchlist_id: {'alert_count': 0, 'has_new_alerts': False} for watchlist_id in watchlist_ids}

    # Get alert counts for each watchlist
    alert_counts = db.session.execute(
        select(Alert.watchlist_id, func.count(Alert.id))
        .filter(Alert.watchlist_id.in_(watchlist_ids))
        .group_by(Alert.watchlist_id)
    ).all()

    # Get a new alert status for each watchlist
    new_alerts = db.session.execute(
        select(Alert.watchlist_id, func.count(Alert.id))
        .filter(Alert.watchlist_id.in_(watchlist_ids), Alert.is_new == True)
        .group_by(Alert.watchlist_id)
    ).all()

    # Update stats with alert counts
    for watchlist_id, count in alert_counts:
        stats[watchlist_id]['alert_count'] = count

    # Update stats with new alert status
    for watchlist_id, count in new_alerts:
        if count > 0:
            stats[watchlist_id]['has_new_alerts'] = True

    return watchlists_pagination, stats
