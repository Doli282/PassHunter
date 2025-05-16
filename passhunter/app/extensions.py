"""Extensions for the PassHunter web application."""
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_moment import Moment

# Initialize the database - SQLAlchemy
migrate = Migrate()

# Initialize security
login = LoginManager()

# Initialize date formatting
moment = Moment()
