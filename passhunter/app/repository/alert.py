"""Repository for Alerts"""
from flask import current_app
from flask_login import current_user
from flask_sqlalchemy.pagination import Pagination
from sqlalchemy import and_

from app import db
from models import Alert, Watchlist


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

def get_alert_by_id(alert_id: int) -> Alert:
    """
    Retrieve Alert by ID.
    Rejects requests for Alerts that do not belong to the current user.

    Args:
        alert_id (int): Alert ID.

    Returns:
        Alert: Alert by ID.
    """
    query = db.select(Alert).join(Watchlist, Alert.watchlist_id == Watchlist.id).filter(
        Alert.id == alert_id,
        Watchlist.account_id == current_user.id
    )
    return db.one_or_404(query)

def change_alert_state(alert_id: int) -> Alert:
    """
    Switch the state of an alert.
    Register an alert if it was new.
    Make the alert new if it was already registered.

    Args:
        alert_id (int): ID of the alert to register.

    Returns:
        Alert: Registered alert.
    """
    alert = get_alert_by_id(alert_id)
    alert.is_new = not alert.is_new
    db.session.commit()
    return alert
