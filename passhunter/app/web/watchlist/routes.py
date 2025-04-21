"""Views for the watchlist page of the PassHunter web application."""
from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from werkzeug import Response

import app.repository.watchlist as watchlist_repository
from app.extensions import db
from app.models.alert import Alert
from app.models.domain import Domain
from app.models.watchlist import Watchlist
from app.web.watchlist import bp
from app.web.watchlist.forms import (
    WatchlistForm,
    DeleteWatchlistForm,
    AddDomainForm,
    RemoveDomainForm
)


@bp.route('/watchlists')
@login_required
def list_watchlists() -> str:
    """
    List all watchlists belonging to the current user in pages.

    Returns:
        str: The watchlist list template.
    """
    page = request.args.get('page', 1, type=int)

    # Get watchlists with alert stats for the current user
    watchlists_pagination, alert_stats = watchlist_repository.get_by_account_id_with_stats(
        current_user.id, page
    )

    return render_template(
        'watchlist/list.html',
        watchlists=watchlists_pagination.items,
        pagination=watchlists_pagination,
        alert_stats=alert_stats
    )
