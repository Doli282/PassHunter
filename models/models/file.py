"""File model"""


from . import db

class File(db.Model):
    """
    File model for the PassHunter web application.
    The file model is used to store the uploaded files.
    Storing the hashes of the uploaded files should limit the number of duplicates.
    """
    __tablename__ = 'file'
    __table_args__ = {'comment': 'Uploaded files'}
    id: db.Mapped[int] = db.mapped_column(db.Integer, primary_key=True, comment='File ID')
    hash: db.Mapped[bytes] = db.mapped_column(db.LargeBinary(64), nullable=False, unique=True, comment='File hash')
    name: db.Mapped[str] = db.mapped_column(db.String(255), nullable=False, unique=False, comment='File name')

    def __repr__(self):
        """Represent the File model as a string."""
        return f'<File hash={self.hash} name={self.name}>'
