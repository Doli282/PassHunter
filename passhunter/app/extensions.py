"""Extensions for the PassHunter web application."""
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

# Initialize the database - SQLAlchemy
db = SQLAlchemy()
migrate = Migrate()

# Initialize security
login = LoginManager()
