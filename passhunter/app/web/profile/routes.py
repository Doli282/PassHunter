"""Views for the profile page of the PassHunter web application."""
from flask import render_template
from flask_login import login_required

from app.repository import account as account_repository
from app.web.profile import bp


@bp.route('/profile/<int:account_id>')
@login_required
def profile(account_id: int) -> str:
    """
    Render the profile page.

    Args:
        account_id (int): The account ID.
    Returns:
        str: The rendered profile page.
    Raises:
        404: If the account ID is not found.
    """
    account = account_repository.get_by_id_404(account_id)
    return render_template('profile/profile.html', account=account)
