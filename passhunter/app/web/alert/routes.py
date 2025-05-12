"""Views for the alert page of the PassHunter web application."""
from dns.name import empty
from flask import request, render_template, redirect, url_for, flash, Response

import app.repository.alert as alert_repository
from app.web import EmptyForm
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
    return render_template('alert/list.html', pagination=pagination, empty_form=EmptyForm())

@bp.route('/alerts/<int:alert_id>/register', methods=['POST'])
def change_alert_state(alert_id: int) -> Response:
    """
    Change the state of an alert.
    Switch between 'new' and 'registered'.

    Args:
        alert_id (int): The ID of the alert to change the state of.

    Returns:
        Response: Redirect to the referrer page or the alert list page.
    """
    alert = alert_repository.change_alert_state(alert_id)
    flash(f"The alert has been set to {alert.print_status()}.")
    return redirect(request.referrer or  url_for('alert.list_alerts'))


