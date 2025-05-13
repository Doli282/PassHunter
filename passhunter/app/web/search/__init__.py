"""Views and routes for search using OpenSearch."""
from flask import Blueprint

bp = Blueprint('search', __name__)

from app.web.search import routes
