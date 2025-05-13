"""Repository for Alerts"""
from flask import current_app
from flask_login import current_user
from flask_sqlalchemy.pagination import Pagination
from sqlalchemy import and_

from app import db
from models import Alert, Watchlist, Domain


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
    """
    Return the number of alerts for a watchlist and domain.
    
    Args:
        watchlist_id (int): Watchlist ID.
        domain_id (int): Domain ID.

    Returns:
        int: Number of alerts.
    """
    if domain_id:
        return get_count_by_domain_and_watchlist(domain_id, watchlist_id)
    else:
        return get_count_by_watchlist(watchlist_id)

def get_new_alert_count() -> int:
    """
    Return the number of new alerts for the current user.

    Returns:
        int: Number of new alerts.
    """
    from app.repository.watchlist import _select_watchlist_ids_for_user
    watchlist_ids = _select_watchlist_ids_for_user(current_user)
    return db.session.scalar(db.select(db.func.count(Alert.id)).filter(and_(Alert.watchlist_id.in_(watchlist_ids), Alert.is_new == True)))

# Following code (function) was created by Cursor IDE.
# AI model: Claude 3.7 Sonnet
# Prompt: Update the alert list template to include a filter form with fields for status, date range, domain name, and
# watchlist name
def _apply_filters(query, filters):
    """
    Apply filters to the alert query.
    Args:
        query: The base query to apply filters to
        filters: Dictionary containing filter values
    Returns:
        The modified query with filters applied
    """
    if filters.get('status') and filters['status'] != 'all':
        is_new = filters['status'] == 'new'
        query = query.filter(Alert.is_new == is_new)
        
    if filters.get('domain_name'):
        query = query.join(Domain).filter(
            Domain.name.ilike(f"%{filters['domain_name']}%")
        )
    elif filters.get('domain_id'):
        query = query.filter(Alert.domain_id == filters['domain_id'])
        
    if filters.get('watchlist_name'):
        query = query.join(Watchlist).filter(
            Watchlist.name.ilike(f"%{filters['watchlist_name']}%")
        )
    elif filters.get('watchlist_id'):
        query = query.filter(Alert.watchlist_id == filters['watchlist_id'])
        
    if filters.get('date_from'):
        query = query.filter(Alert.created_at >= filters['date_from'])
        
    if filters.get('date_to'):
        query = query.filter(Alert.created_at <= filters['date_to'])
        
    return query

# Following code (function) was created by Cursor IDE.
# AI model: Claude 3.7 Sonnet
# Prompt: Update the alert list template to include a filter form with fields for status, date range, domain name, and
# watchlist name
def get_page_all(page: int = 1, filters: dict = None) -> Pagination:
    """
    Retrieve paginated all Alerts for the current user with optional filters.
    Args:
        page (int): Page number.
        filters (dict): Dictionary containing filter values
    Returns:
        Pagination: Paginated Alerts.
    """
    from app.repository.watchlist import _select_watchlists_for_user
    watchlists = _select_watchlists_for_user(current_user).subquery()
    query_alerts = db.select(Alert).join(watchlists, Alert.watchlist_id == watchlists.c.id)
    
    # Apply filters if provided
    if filters:
        query_alerts = _apply_filters(query_alerts, filters)
        
    query_alerts = query_alerts.order_by(Alert.is_new.desc(), Alert.created_at.desc())
    
    # Get total count to validate page number
    total = db.session.scalar(db.select(db.func.count()).select_from(query_alerts.subquery()))
    per_page = current_app.config['PER_PAGE']
    max_page = (total + per_page - 1) // per_page if total > 0 else 1
    
    # If page is invalid, default to page 1
    if page < 1 or page > max_page:
        page = 1
        
    return db.paginate(select=query_alerts, page=page, max_per_page=per_page)

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

def delete_alert(alert: Alert) -> Alert:
    """
    Remove alert from the database.

    Args:
        alert (Alert): Alert to delete.

    Returns:
        Alert: deleted alert.
    """
    db.session.delete(alert)
    db.session.commit()
    return alert