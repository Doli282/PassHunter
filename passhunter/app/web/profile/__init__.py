"""Blueprint for the profile page of the PassHunter web application."""
from flask import Blueprint

bp = Blueprint('profile', __name__)

from app.web.profile import routes
