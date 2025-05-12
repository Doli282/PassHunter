"""Views for the alert page of the PassHunter web application."""
from flask import request, render_template, redirect, url_for, flash, Response
from flask_login import login_required

import app.repository.alert as alert_repository
from app.web import EmptyForm
from app.web.alert import bp
from app.web.alert.forms import AlertFilterForm

# Following function was created by Cursor IDE.
# AI model: Claude 3.7 Sonnet
# Prompt: Update the alert routes to handle filter form submission and process filters for status, date range, domain name, and watchlist name
@bp.route('/alerts', methods=['GET', 'POST'])
@login_required
def list_alerts() -> str | Response:
    """
    List all alerts belonging to the current user.
    Supports filtering of alerts based on various criteria.

    Returns:
        str | Response: The rendered template for the alert list page or a redirect response.
    """
    page = request.args.get('page', 1, type=int)
    filter_form = AlertFilterForm()
    filters = {}
    filter_values = {}

    if request.method == 'POST':
        if filter_form.reset.data:
            return redirect(url_for('alert.list_alerts'))
            
        if filter_form.validate_on_submit():
            if filter_form.status.data != 'all':
                filters['status'] = filter_form.status.data
            if filter_form.domain_name.data:
                filters['domain_name'] = filter_form.domain_name.data
            if filter_form.watchlist_name.data:
                filters['watchlist_name'] = filter_form.watchlist_name.data
            if filter_form.date_from.data:
                filters['date_from'] = filter_form.date_from.data
            if filter_form.date_to.data:
                filters['date_to'] = filter_form.date_to.data
                
            # Convert datetime objects to strings for template use
            for k, v in filters.items():
                if hasattr(v, 'strftime'):
                    filter_values[k] = v.strftime('%Y-%m-%dT%H:%M')
                else:
                    filter_values[k] = v
                    
            pagination = alert_repository.get_page_all(page, filters)
        else:
            pagination = alert_repository.get_page_all(page)
    else:
        # Pre-populate form with query parameters if they exist
        filter_form.status.data = request.args.get('status', 'all')
        filter_form.domain_name.data = request.args.get('domain_name', '')
        filter_form.watchlist_name.data = request.args.get('watchlist_name', '')
        if request.args.get('date_from'):
            filter_form.date_from.data = request.args.get('date_from')
        if request.args.get('date_to'):
            filter_form.date_to.data = request.args.get('date_to')
            
        # Apply filters from query parameters
        if filter_form.status.data != 'all':
            filters['status'] = filter_form.status.data
        if filter_form.domain_name.data:
            filters['domain_name'] = filter_form.domain_name.data
        if filter_form.watchlist_name.data:
            filters['watchlist_name'] = filter_form.watchlist_name.data
        if filter_form.date_from.data:
            filters['date_from'] = filter_form.date_from.data
        if filter_form.date_to.data:
            filters['date_to'] = filter_form.date_to.data
            
        # Convert datetime objects to strings for template use
        for k, v in filters.items():
            if hasattr(v, 'strftime'):
                filter_values[k] = v.strftime('%Y-%m-%dT%H:%M')
            else:
                filter_values[k] = v
                
        pagination = alert_repository.get_page_all(page, filters)
    
    return render_template('alert/list.html', 
                         pagination=pagination, 
                         empty_form=EmptyForm(),
                         filter_form=filter_form,
                         filter_values=filter_values)

@bp.route('/alerts/<int:alert_id>/register', methods=['POST'])
@login_required
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

    # Following function was created by Cursor IDE.
    # AI model: Claude 3.5 Sonnet
    # Prompt: Update the alert routes to handle filter form submission and process filters for status, date range, domain name, and watchlist name
    # Preserve filters when redirecting
    filters = {}
    for key in ['status', 'domain_name', 'watchlist_name', 'date_from', 'date_to']:
        value = request.form.get(key)
        if value:
            filters[key] = value

    return redirect(request.referrer or url_for('alert.list_alerts', **filters))


