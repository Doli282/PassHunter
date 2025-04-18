"""Blueprint for the authentication of the PassHunter web application."""
from flask import Blueprint

bp = Blueprint('auth', __name__)

from app.web.auth import routes
