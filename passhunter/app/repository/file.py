"""Repository for File"""

from app import db
from models import File


def get_files_count() -> int:
    """
    Returns the number of files in the database.

    Returns:
         int: Number of files in the database.
    """
    return db.session.scalar(db.select(db.func.count(File.id)))
