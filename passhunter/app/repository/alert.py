"""Repository for Alerts"""
from flask import current_app
from flask_login import current_user
from flask_sqlalchemy.pagination import Pagination
from sqlalchemy import and_

from app import db
from models import Alert

def get_count_by_watchlist(watchlist_id: int) -> int:
    """
    Return the number of alerts for a watchlist.

    Args:
        watchlist_id (int): Watchlist ID.

    Returns:
        int: Number of alerts.
    """
    return db.session.scalar(db.select(db.func.count(Alert.id)).filter(Alert.watchlist_id == watchlist_id))

def get_count_by_domain_and_watchlist(domain_id: int, watchlist_id: int) -> int:
    """
    Return the number of alerts for a domain and watchlist.

    Args:
        domain_id (int): Domain ID.
        watchlist_id (int): Watchlist ID.

    Returns:
        int: Number of alerts.
    """
    return db.session.scalar(db.select(db.func.count(Alert.id)).filter(and_(Alert.domain_id == domain_id, Alert.watchlist_id == watchlist_id)))

def get_alert_count(watchlist_id: int, domain_id: int = None) -> int:
    if domain_id:
        return get_count_by_domain_and_watchlist(domain_id, watchlist_id)
    else:
        return get_count_by_watchlist(watchlist_id)

def get_page_all(page: int = 1) -> Pagination:
    """
    Retrieve paginated all Alerts for the current user.

    Args:
        page (int): Page number.

    Returns:
        Pagination: Paginated Alerts.
    """
    from app.repository.watchlist import _select_watchlists_for_user
    # Get all watchlists for the current user
    watchlists = _select_watchlists_for_user(current_user).subquery()
    # Get all alerts
    query_alerts = db.select(Alert).join(watchlists, Alert.watchlist_id == watchlists.c.id)
    return db.paginate(select=query_alerts, page=page,max_per_page=current_app.config['PER_PAGE'])
