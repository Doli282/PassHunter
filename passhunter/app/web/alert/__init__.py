"""Blueprint for the alert page of the PassHunter web application."""
from flask import Blueprint

bp = Blueprint('alert', __name__)

from app.web.alert import routes
