from urllib.parse import urlparse
from src.models import Source, Coupon, Coupon, db, session
from flask_login import current_user
from flask_paginate import Pagination

class CouponsModule(object):
    """Coupons Module
    """
    def __init__(self):
        pass

    def get_all(self):
        return Coupon.query.all()

    def get(self, id):
        return Coupon.query.get(id)

    def search(self, **kwargs):
        page = kwargs.get('page', 1)
        per_page = kwargs.get('per_page', 20)
        search = kwargs.get('search', False)
        # file_id = kwargs.get("file_id")

        # if file_id:
        #     leads = Lead.query.order_by(Lead.created_at.desc()).filter(Lead.file_id==file_id)
        #     pagination = Pagination(page=page, total=leads.count(), search=search, record_name='leads', css_framework='bootstrap3')
        #     return (pagination, leads.paginate(page, per_page, error_out=search).items)
        # else:
        
        coupons = Coupon.query.order_by(Coupon.created_at.desc())
        pagination = Pagination(page=page, per_page=per_page, total=coupons.count(), search=search, record_name='coupons', css_framework='bootstrap3')
        return (pagination, coupons.paginate(page, per_page, error_out=search).items)

