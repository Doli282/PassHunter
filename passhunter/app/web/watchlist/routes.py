"""Views for the watchlist page of the PassHunter web application."""
from flask import render_template, redirect, url_for, flash
from app.models.alert import Alert
from app.models.watchlist import Watchlist
from app.models.domain import Domain
from app.extensions import db
from app.web.watchlist import bp
from app.web.watchlist.forms import (
    WatchlistForm,
    DeleteWatchlistForm,
    AddDomainForm,
    RemoveDomainForm
)

@bp.route('/watchlists')
def list_watchlists():
    """
    List all watchlists.

    Returns:
        The watchlist list template.
    """
    watchlists = Watchlist.query.all()
    return render_template('watchlist/list.html', watchlists=watchlists)

@bp.route('/watchlists/<int:watchlist_id>')
def view_watchlist(watchlist_id: int):
    """
    View a specific watchlist.

    Args:
        watchlist_id (int): The ID of the watchlist to view.
    Returns:
        The watchlist view template.
    """
    watchlist = Watchlist.query.get_or_404(watchlist_id)
    add_domain_form = AddDomainForm()
    alerts = []
    for domain in watchlist.domains:
        alerts += Alert.query.filter_by(domain_id=domain.id).all()
    return render_template(
        'watchlist/view.html',
        watchlist=watchlist,
        add_domain_form=add_domain_form
    )

@bp.route('/watchlists/create', methods=['GET', 'POST'])
def create_watchlist():
    """
    Create a new watchlist.

    Returns:
        The watchlist create template.
    """
    form = WatchlistForm()
    if form.validate_on_submit():
        watchlist = Watchlist(
            name=form.name.data,
            description=form.description.data,
            is_active=form.is_active.data,
            mail_address=form.mail_address.data,
            mail_alerts=form.mail_alerts.data
        )
        db.session.add(watchlist)
        db.session.commit()
        flash('Watchlist created successfully', 'success')
        return redirect(url_for('watchlist.view_watchlist', watchlist_id=watchlist.id))
    return render_template('watchlist/create.html', form=form)

@bp.route('/watchlists/<int:watchlist_id>/edit', methods=['GET', 'POST'])
def edit_watchlist(watchlist_id: int):
    """Edit an existing watchlist."""
    watchlist = Watchlist.query.get_or_404(watchlist_id)
    form = WatchlistForm(obj=watchlist)
    if form.validate_on_submit():
        form.populate_obj(watchlist)
        db.session.commit()
        flash('Watchlist updated successfully', 'success')
        return redirect(url_for('watchlist.view_watchlist', watchlist_id=watchlist.id))
    return render_template('watchlist/edit.html', form=form, watchlist=watchlist)

@bp.route('/watchlists/<int:watchlist_id>/confirm-delete', methods=['GET'])
def confirm_delete_watchlist(watchlist_id: int):
    """Show confirmation page for watchlist deletion."""
    watchlist = Watchlist.query.get_or_404(watchlist_id)
    form = DeleteWatchlistForm()
    return render_template('watchlist/confirm_delete_watchlist.html', watchlist=watchlist, form=form)

@bp.route('/watchlists/<int:watchlist_id>/delete', methods=['POST'])
def delete_watchlist(watchlist_id: int):
    """Delete a watchlist."""
    form = DeleteWatchlistForm()
    if form.validate_on_submit():
        watchlist = Watchlist.query.get_or_404(watchlist_id)
        db.session.delete(watchlist)
        db.session.commit()
        flash('Watchlist deleted successfully', 'success')
    return redirect(url_for('watchlist.list_watchlists'))

@bp.route('/watchlists/<int:watchlist_id>/add-domain', methods=['GET', 'POST'])
def add_domain(watchlist_id: int):
    """Add a domain to a watchlist."""
    watchlist = Watchlist.query.get_or_404(watchlist_id)
    form = AddDomainForm()
    if form.validate_on_submit():
        domain = Domain.query.filter_by(name=form.domain.data).first()
        if not domain:
            domain = Domain(name=form.domain.data)
            db.session.add(domain)
        
        if domain not in watchlist.domains:
            watchlist.domains.append(domain)
            db.session.commit()
            flash('Domain added to watchlist successfully', 'success')
        else:
            flash('Domain is already in the watchlist', 'warning')
        
        return redirect(url_for('watchlist.view_watchlist', watchlist_id=watchlist_id))
    return render_template('watchlist/add_domain.html', form=form, watchlist=watchlist)

@bp.route('/watchlists/<int:watchlist_id>/confirm-delete-domain/<int:domain_id>', methods=['GET'])
def confirm_delete_domain(watchlist_id: int, domain_id: int):
    """Show confirmation page for domain removal."""
    watchlist = Watchlist.query.get_or_404(watchlist_id)
    domain = Domain.query.get_or_404(domain_id)
    form = RemoveDomainForm()
    return render_template('watchlist/confirm_delete_domain.html', watchlist=watchlist, domain=domain, form=form)

@bp.route('/watchlists/<int:watchlist_id>/remove-domain/<int:domain_id>', methods=['POST'])
def remove_domain(watchlist_id: int, domain_id: int):
    """Remove a domain from a watchlist."""
    form = RemoveDomainForm()
    if form.validate_on_submit():
        watchlist = Watchlist.query.get_or_404(watchlist_id)
        domain = Domain.query.get_or_404(domain_id)
        
        if domain in watchlist.domains:
            watchlist.domains.remove(domain)
            db.session.commit()
            flash('Domain removed from watchlist successfully', 'success')
        else:
            flash('Domain is not in the watchlist', 'error')
    
    return redirect(url_for('watchlist.view_watchlist', watchlist_id=watchlist_id)) 