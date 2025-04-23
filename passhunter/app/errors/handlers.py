"""Define custom error handlers."""
from flask import render_template

from app import db
from app.errors import bp


@bp.app_errorhandler(404)
def not_found(error: Exception) -> tuple[str, int]:
    """
    404 Not Found

    Custom error handler for 404.

    Args:
        error (Exception): Exception raised by this handler.
    Returns:
        tuple[str, int]: Custom error template and error code.
    """
    return render_template('errors/404.html'), 404


@bp.app_errorhandler(500)
def internal_server_error(error: Exception) -> tuple[str, int]:
    """
    500 Internal Server Error

    Custom error handler for 500.
    Roll bach the database.

    Args:
        error (Exception): Exception raised by this handler.
    Returns:
        tuple[str, int]: Custom error template and error code.
    """
    db.session.rollback()
    return render_template('errors/500.html'), 500
