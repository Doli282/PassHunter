"""Initialize the PassHunter web application."""
from flask import Flask
from config import Config
#from app.extensions import db

def create_app():
    """Create and configure the Flask application."""
    app = Flask(__name__)
    app.config.from_object(Config)
    
    from app.routes import bp as main_bp
    app.register_blueprint(main_bp)

    #db.init_app(app)
    return app
