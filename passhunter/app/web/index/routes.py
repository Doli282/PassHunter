"""Views for the index page of the PassHunter web application."""
from flask import render_template

from app.repository import file as file_repository
from app.web.index import bp

@bp.route('/')
@bp.route('/index')
def index() -> str:
    """
    Render the index page.

    Returns:
        str: The rendered index page.
    """
    no_files = file_repository.get_files_count()
    return render_template('index.html', no_files=no_files)
