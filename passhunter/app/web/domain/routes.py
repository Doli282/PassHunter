"""Views for the watchlist page of the PassHunter web application."""

from flask import render_template, request
from flask_login import login_required

from app.web import EmptyForm
from app.web.domain import bp as bp_domains
from app.repository import domain as domain_repository
from app.repository import alert as alert_repository

@bp_domains.route('/domains')
@login_required
def list_domains() -> str:
    """
    View a list of domains monitored by the current user.

    Returns:
        str: The rendered template for the domain list page.
    """
    page = request.args.get('page', 1, type=int)
    pagination = domain_repository.get_page_all(page)
    return render_template(
        'domain/list.html',
        pagination=pagination
    )


@bp_domains.route('/domains/<int:domain_id>')
@login_required
def view_domain(domain_id: int) -> str:
    """
    View details about a specific domain monitored by the current user.

    Args:
        domain_id (int): The ID of the domain to view.
    Returns:
        str: The rendered template for the domain view page.
    Raises:
        404 Not Found: If the domain with the specified ID does not exist.
    """
    domain = domain_repository.get_by_id(domain_id)
    page = request.args.get('page', 1, type=int)
    filters = {'domain_id': domain_id}
    pagination = alert_repository.get_page_all(page, filters)
    
    return render_template('domain/view.html', domain=domain, pagination=pagination, empty_form=EmptyForm())