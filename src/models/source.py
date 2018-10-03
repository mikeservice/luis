"""Source Model
"""
from .__include__ import *

class Source(db.Model):
    """sources table
    """
    __tablename__ = 'sources'

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(30), unique = True, nullable=False)
    base_url = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow())
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow())
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    updated_by = db.Column(db.Integer, db.ForeignKey('users.id'))

    stores = db.relationship("Store", backref="source", lazy="dynamic")

    def __init__(self, **kwargs):
        self.name = kwargs.get("name", None)
        self.base_url = kwargs.get("base_url", None)

