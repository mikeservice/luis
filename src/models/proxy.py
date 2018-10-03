"""Proxy Model
"""
from .__include__ import *

class Proxy(db.Model):
    """proxies table
    """
    __tablename__ = 'proxies'

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(30), unique = True, nullable=False)
    source = db.Column(db.String(20), nullable=False, default='myprivatevpn')
    status = db.Column(db.String(10), nullable=False, default='active')
    used_at = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow())

    def __init__(self, **kwargs):
        self.name = kwargs.get("name", None)
        self.source = kwargs.get("source", None)
        self.status = kwargs.get("status", None)

    @staticmethod
    def last():
        c = Proxy.query.filter(and_(Proxy.status=="active")).order_by(asc(Proxy.used_at)).limit(1).first()
        if c:
            c.used_at = datetime.datetime.utcnow()
            session.commit()
        
        return c

    @staticmethod
    def mark_as(id, status='active'):
        p = Proxy.query.get(id)
        p.status = status

        try:
            session.commit()
            return True
        except Exception as e:
            print(str(e))
            session.rollback()
            return False

