"""Extensions for the PassHunter web application."""
from flask_login import LoginManager
from flask_migrate import Migrate

# Initialize the database - SQLAlchemy
migrate = Migrate()

# Initialize security
login = LoginManager()
