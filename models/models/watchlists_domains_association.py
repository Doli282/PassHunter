"""Association table for the many-to-many relationship between Watchlist and Domain."""
from . import db

# Association table for many-to-many relationship between Watchlist and Domain
watchlist_domain_association = db.Table('watchlist_domain_association',
                                        db.metadata,
                                        db.Column('watchlist_id', db.Integer,
                                                  db.ForeignKey('watchlist.id', ondelete='CASCADE'), primary_key=True),
                                        db.Column('domain_id', db.Integer,
                                                  db.ForeignKey('domain.id', ondelete='CASCADE'), primary_key=True),
                                        db.UniqueConstraint('watchlist_id', 'domain_id', name='uq_watchlist_domain')
                                        )
