"""Store Model
"""
from .__include__ import *

class StoreStatus(object):
    def __init__(self):
        pass

    initial = None
    pending = 'pending'
    working = 'working'
    done = 'done'


class Store(db.Model):
    """stores table
    """
    __tablename__ = 'stores'

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(30), unique = True, nullable=False)
    start_point = db.Column(db.Text, nullable=False)
    job_uid = db.Column(db.String(60))
    status = db.Column(db.String(10))
    source_id = db.Column(db.Integer, db.ForeignKey('sources.id'))
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow())
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow())

    coupons = db.relationship("Coupon", backref="store", lazy="dynamic")

    def __init__(self, **kwargs):
        self.name = kwargs.get("name", None)
        self.start_point = kwargs.get("start_point", None)
        self.source_id = kwargs.get("source_id", None)

    @property
    def as_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "start_point": self.start_point,
            "status": self.status,
            "source": self.source.name
        }

    @staticmethod
    def clean():
        count = 0
        for s in Store.query.filter(or_(Store.status==StoreStatus.pending, Store.status==StoreStatus.working)).all():
            s.job_uid = None
            count += 1
        
        return count
