"""Repository for Watchlist"""
from flask import current_app
from flask_login import current_user
from flask_sqlalchemy.pagination import Pagination
from sqlalchemy import and_, Select

from app import db
from models import Account, Domain
from models.watchlist import Watchlist
from app.web.watchlist.forms import WatchlistForm


def _select_watchlists_for_user(user: Account) -> Select:
    """
    Select Watchlists for a user.

    Args:
        user (Account): Owner of the Watchlists.
    Returns:
        Select: SQLAlchemy select statement.
    """
    return db.select(Watchlist).filter(Watchlist.account_id == user.id)


def get_page(page: int = 1) -> Pagination:
    """
    Retrieve paginated Watchlists of the current user.

    Args:
        page (int): Page number.
    Returns:
        Pagination: Paginated Watchlists.
    """
    query = _select_watchlists_for_user(current_user)
    return db.paginate(select=query, page=page, max_per_page=current_app.config['PER_PAGE'])


def get_by_id(watchlist_id: int) -> Watchlist:
    """
    Retrieve Watchlist by ID.
    Rejects requests for Watchlists that do not belong to the current user.

    Args:
        watchlist_id (int): Watchlist ID.
    Returns:
        Watchlist: Watchlist by ID.
    Raises:
        404 Not Found: If no Watchlist is found for the given ID.
    """
    query = db.select(Watchlist).filter(and_(Watchlist.id == watchlist_id, Watchlist.account_id == current_user.id))
    return db.one_or_404(query)


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


def update(form: WatchlistForm, watchlist: Watchlist) -> Watchlist:
    """
    Update an existing Watchlist.

    Args:
        form (WatchlistForm): Watchlist form.
        watchlist (Watchlist): Watchlist to update.
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
    Raises:
        404 Not Found: If no Watchlist is found for the given ID.
    """
    watchlist = get_by_id(watchlist_id)
    db.session.delete(watchlist)
    db.session.commit()
    return watchlist
