"""Repository for Watchlist"""
from typing import List

from flask import current_app
from flask_sqlalchemy.pagination import Pagination

from app import db
from app.models import Account
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
    return db.get_or_404(Watchlist, ident=watchlist_id)


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
    """
    watchlist = get_by_id(watchlist_id)
    db.session.delete(watchlist)
    db.session.commit()
    return watchlist
