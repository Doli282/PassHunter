"""Command-line interface for managing the application."""
from flask.cli import FlaskGroup

from app import create_app
from models import db

cli = FlaskGroup(create_app())

@cli.command("create_db")
def create_db():
    db.drop_all()
    db.create_all()
    db.session.commit()
    print("Database created")

if __name__ == "__main__":
    cli()