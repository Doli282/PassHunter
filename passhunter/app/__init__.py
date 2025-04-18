"""Initialize the PassHunter web application."""
from flask import Flask

from app.extensions import db, migrate, login
from config import Config


def create_app():
    """Create and configure the Flask application."""
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)
    login.login_view = 'auth.login'
    # TODO look at other security settings
    # https://flask-login.readthedocs.io/en/latest/
    login.session_protection = 'strong'

    # Register the blueprints
    from app.web.index import bp as home_bp
    app.register_blueprint(home_bp)

    from app.web.auth import bp as auth_bp
    app.register_blueprint(auth_bp)

    from app.web.watchlist import bp as watchlist_bp
    app.register_blueprint(watchlist_bp)

    return app
