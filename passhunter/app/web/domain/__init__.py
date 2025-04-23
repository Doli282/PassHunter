"""Blueprint for the domain page of the PassHunter web application."""
from flask import Blueprint

bp = Blueprint('domain', __name__)

from app.web.domain import routes
