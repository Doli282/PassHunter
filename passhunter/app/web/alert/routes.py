"""Views for the alert page of the PassHunter web application."""
from flask import request, render_template

import app.repository.alert as alert_repository
from app.web.alert import bp

@bp.route('/alerts')
def list_alerts() -> str:
    """
    List all alerts belonging to the current user.

    Returns:
        str: The rendered template for the alert list page.
    """
    page = request.args.get('page', 1, type=int)
    pagination = alert_repository.get_page_all(page)
    return render_template('alert/list.html', pagination=pagination)