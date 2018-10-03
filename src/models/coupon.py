"""Coupon Model
"""
from .__include__ import *

class Coupon(db.Model):
    """coupons table
    """
    __tablename__ = 'coupons'

    id = db.Column(db.Integer, primary_key = True)
    original_title = db.Column(db.String(100), nullable=True)
    title = db.Column(db.String(100), nullable=False)
    title_changed = db.Column(db.Boolean, default=False)
    original_description = db.Column(db.Text, nullable=True)
    description = db.Column(db.Text, nullable=True)
    description_changed = db.Column(db.Boolean, default=False)
    price = db.Column(db.String(30), nullable=False)
    expiry_date = db.Column(db.String(20), nullable=False)
    url = db.Column(db.Text, nullable=False)
    code = db.Column(db.String(50), nullable=True)
    store_id = db.Column(db.Integer, db.ForeignKey('stores.id'))
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow())

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if not self.expiry_date:
            self.expiry_date = (datetime.date.today() + datetime.timedelta(days=7)).strftime('%Y/%m/%d')
        else:
            self.expiry_date = parse(self.expiry_date).strftime("%Y/%m/%d")

    @property
    def as_dict(self):
        return {
            "title": self.title,
            "description": self.description,
            "title_changed": self.title_changed,
            "description_changed": self.description_chantitle_changed,
            "price": self.price,
            "expiry_date": self.expiry_date,
            "url": self.url,
            "code": self.code,
            "store": self.store
        }

