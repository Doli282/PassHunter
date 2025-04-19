"""Blueprint for the index page of the PassHunter web application."""
from flask import Blueprint

bp = Blueprint('index', __name__)

from app.web.index import routes
