"""Routes for the PassHunter web application."""
from flask import Blueprint

bp = Blueprint('main', __name__)

from app.routes import hello_world_route