"""Log Model
"""
from .__include__ import *

class Log(db.Model):
    """logs table
    """
    __tablename__ = 'logs'

    id = db.Column(db.Integer, primary_key = True)
    subject = db.Column(db.String(30), nullable=False)
    content = db.Column(db.Text, nullable=False)
    level = db.Column(db.String(20), nullable=False, default='info')
    status = db.Column(db.String(10), nullable=False, default="active")
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow())
    solved_at = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow())
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    solved_by = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

