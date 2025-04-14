"""Association table for the many-to-many relationship between Domains and Watchlists."""
from app.extensions import db
#from sqlalchemy import event, Mapper, delete
#from sqlalchemy.engine import Connection
#from sqlalchemy.engine import Row
#from app.models.domain import Domain

# Association table for many-to-many relationship between Watchlist and Domain
watchlist_domain_association = db.Table('watchlist_domain_association',
    db.Column('watchlist_id', db.Integer, db.ForeignKey('watchlist.id', ondelete='CASCADE'), primary_key=True),
    db.Column('domain_id', db.Integer, db.ForeignKey('domain.id', ondelete='CASCADE'), primary_key=True),
    db.UniqueConstraint('watchlist_id', 'domain_id', name='uq_watchlist_domain')
)

#@event.listens_for(watchlist_domain_association, 'after_delete')
#def delete_orphaned_domain(mapper: Mapper, connection: Connection, target: Row[tuple[int, int]]) -> None:
#    """Delete a domain if it's no longer associated with any watchlist."""
#    domain_id: int = target.domain_id
#    
#    # Check if the domain still has any watchlists
#    remaining_watchlists = connection.execute(
#        watchlist_domain_association.select().where(
#            watchlist_domain_association.c.domain_id == domain_id
#        )
#    ).fetchone()
#    
#    # If no watchlists remain, delete the domain
#    if not remaining_watchlists:
#        stmt = delete(Domain).where(Domain.id == domain_id)
#        connection.execute(stmt) 