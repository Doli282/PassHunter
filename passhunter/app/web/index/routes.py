"""Views for the index page of the PassHunter web application."""
from flask import render_template

from app.web.index import bp


@bp.route('/')
@bp.route('/index')
def index() -> str:
    """
    Render the index page.

    Returns:
        str: The rendered index page.
    """
    return render_template('index.html')
