"""Initialize the PassHunter web application."""
from flask import Flask

from app.extensions import migrate, login
from app.tools.logs import set_mail_error_reporting, set_rotating_log_file
from config import Config
from models import db


def create_app():
    """Create and configure the Flask application."""
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize extensions
    # Initialize Flask-SQLAlchemy
    db.init_app(app)
    migrate.init_app(app, db)
    with app.app_context():
        db.create_all()

    # Initialize Flask-Login
    login.init_app(app)
    login.login_view = 'auth.login'
    # TODO look at other security settings
    # https://flask-login.readthedocs.io/en/latest/
    login.session_protection = 'strong'

    # Register functions into jinja templates
    from app.repository.alert import get_alert_count
    app.jinja_env.globals.update(alert_count=get_alert_count)

    # Register the blueprints
    from app.errors import bp as errors_bp
    app.register_blueprint(errors_bp)

    from app.web.index import bp as home_bp
    app.register_blueprint(home_bp)

    from app.web.auth import bp as auth_bp
    app.register_blueprint(auth_bp)

    from app.web.watchlist import bp as watchlist_bp
    app.register_blueprint(watchlist_bp)

    from app.web.profile import bp as profile_bp
    app.register_blueprint(profile_bp)

    from app.web.domain import bp as domain_bp
    app.register_blueprint(domain_bp)

    # Set logging handlers
    if not app.debug:
        set_mail_error_reporting(app)
        set_rotating_log_file(app)

        app.logger.setLevel('INFO')
        app.logger.info('PassHunter has started')

    return app
