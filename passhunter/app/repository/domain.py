"""Repository for Domain"""
from flask import current_app
from flask_login import current_user
from flask_sqlalchemy.pagination import Pagination


from app import db
from models import Domain, Watchlist
from models.watchlists_domains_association import watchlist_domain_association
from app.repository.watchlist import _select_watchlists_for_user
from app.web.domain.forms import DomainForm


def get_by_id(domain_id: int) -> Domain:
    """
    Retrieve Domain by ID.
    Rejects requests for Domains that do not belong to the current user.

    Args:
        domain_id (int): Domain ID.
    Returns:
        Domain: Domain by ID.
    Raises:
        404 Not Found: If no Domain is found for the given ID.
    """
    # Get all watchlists for the current user
    watchlists = _select_watchlists_for_user(current_user).subquery()
    # Get the domain by ID
    domain = db.select(Domain).filter(Domain.id == domain_id)
    # Join the domain to the watchlists to check if the user owns the domain
    query = domain.join(watchlist_domain_association, Domain.id == watchlist_domain_association.c.domain_id). \
    join(watchlists, watchlist_domain_association.c.watchlist_id == watchlists.c.id)
    # Return the domain if it exists and the user owns it, otherwise raise 404 error
    from passhunter import app
    app.logger.debug(f"DOMAIN ID: {domain_id}")
    app.logger.debug(f"Query: {query}")
    return db.first_or_404(query)


def get_by_name(name: str) -> Domain|None:
    """
    Retrieve Domain by name.
    Search is NOT limited to the current user.

    Args:
        name (str): Domain name.
    Returns:
        Domain|None: Domain by name or None if not found.
    """
    query = db.select(Domain).filter(Domain.name == name)
    return db.session.scalar(query)

def get_page_all(page: int = 1) -> Pagination:
    """
    Retrieve paginated all Domains for the current user.

    Args:
        page (int): Page number.
    Returns:
        Pagination: Paginated Domains.
    """
    # Get all watchlists for the current user
    #watchlist_ids = db.select(Watchlist.id).filter(Watchlist.account_id == current_user.id)
    watchlists = _select_watchlists_for_user(current_user).subquery()
    # Get all domains in the watchlists
    query_domains = db.select(Domain).distinct().join(watchlist_domain_association, Domain.id == watchlist_domain_association.c.domain_id). \
    join(watchlists, watchlist_domain_association.c.watchlist_id == watchlists.c.id).order_by(Domain.id)
    # Return the paginated list of all domains
    return db.paginate(select=query_domains, page=page, max_per_page=current_app.config['PER_PAGE'])


def get_page_for_watchlist(watchlist_id: int, page: int = 1) -> Pagination:
    """
    Retrieve paginated Domains in the watchlist.

    Args:
        watchlist_id (int): Watchlist ID.
        page (int): Page number.
    Returns:
        Pagination: Paginated Domains.
    """
    # Get all domains in the watchlist
    query = db.select(Domain).join(watchlist_domain_association, Domain.id == watchlist_domain_association.c.domain_id).\
    filter(watchlist_domain_association.c.watchlist_id == watchlist_id)
    return db.paginate(select=query, page=page, max_per_page=current_app.config['PER_PAGE'])


def upsert(form: DomainForm, watchlist: Watchlist) -> Domain:
    """
    Create a new Domain.
    If the domain already exists, update the existing domain.

    Args:
        form (DomainForm): Domain form.
        watchlist (Watchlist): Watchlist to associate the domain with.
    Returns:
        Domain: New Domain.
    """
    # Check if the domain already exists
    domain = get_by_name(form.name.data)
    # Create a new domain if it does not exist
    if not domain:
        domain = Domain()
        # Populate the domain from the form
        form.populate_obj(domain)
    # Associate the domain with the watchlist
    domain.watchlists.add(watchlist)
    # Add the domain to the session and commit the changes
    db.session.add(domain)
    db.session.commit()
    return domain


def delete(domain: Domain) -> Domain:
    """
    Delete domain.

    Args:
        domain (Domain): Domain to be deleted.
    Returns:
        Domain: Deleted domain.
    """
    db.session.delete(domain)
    db.session.commit()
    return domain


def remove_domain_from_watchlist(domain: Domain, watchlist: Watchlist) -> Domain:
    """
    Remove domain from the watchlist.
    If the domain has no associated watchlists, delete it.

    Args:
        domain (Domain): Domain to be removed from the watchlist.
        watchlist (Watchlist): Watchlist to be removed from the domain.
    Returns:
        Domain: Updated domain.
    """
    # Remove the domain from the watchlist
    domain.watchlists.discard(watchlist)
    # If the domain has no associated watchlists, delete it
    if not domain.watchlists:
        delete(domain)
    db.session.commit()
    return domain

