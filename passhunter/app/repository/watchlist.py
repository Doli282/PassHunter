"""Repository for Watchlist"""
from typing import List

from app import db
from app.models.watchlist import Watchlist
from app.web.watchlist.forms import WatchlistForm


def get_all() -> List[Watchlist]:
    """
    Retrieve all Watchlists.

    Returns:
        List[Watchlist]: List of all Watchlists.
    """
    # TODO pagination
    return Watchlist.query.all()


def get_by_id(watchlist_id: int) -> Watchlist:
    """
    Retrieve Watchlist by ID.

    Args:
        watchlist_id (int): Watchlist ID.
    Returns:
        Watchlist: Watchlist by ID.
    """
    return db.get_or_404(Watchlist, id=watchlist_id)


def create(form: WatchlistForm) -> Watchlist:
    """
    Create a new Watchlist.

    Args:
        form (WatchlistForm): Watchlist form.
    Returns:
        Watchlist: New Watchlist.
    """
    watchlist = Watchlist(
        name=form.name.data,
        description=form.description.data,
        is_active=form.is_active.data,
        email=form.email.data,
        send_alerts=form.send_alerts.data
    )
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
