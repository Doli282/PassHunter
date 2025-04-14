"""Blueprint for the watchlist page of the PassHunter web application."""
from flask import Blueprint

bp = Blueprint('watchlist', __name__)

from app.web.watchlist import routes
