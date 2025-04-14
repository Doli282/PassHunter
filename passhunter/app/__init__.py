"""Initialize the PassHunter web application."""
from flask import Flask
from config import Config
from app.extensions import db, migrate

def create_app():
    """Create and configure the Flask application."""
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize the extensions
    db.init_app(app)
    migrate.init_app(app, db)

    # Register the blueprints
    from app.web.index import bp as home_bp
    app.register_blueprint(home_bp)

    from app.web.watchlist import bp as watchlist_bp
    app.register_blueprint(watchlist_bp)


    return app
