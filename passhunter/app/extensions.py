"""Extensions for the PassHunter web application."""
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# Initialize the database - SQLAlchemy
db = SQLAlchemy()
migrate = Migrate()
