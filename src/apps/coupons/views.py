"""
Views for admin/source_app
"""

import datetime, json, requests

from flask import request, render_template, url_for, redirect, jsonify
from flask_paginate import Pagination, get_page_parameter

from src.libs import AuthorizedView
from .modules import CouponsModule

class CouponsView(AuthorizedView):
    """
    View for dashboard
    """
    def __init__(self, **kwargs):
        super().__init__()
        self.per_page = kwargs.get("per_page", 20)
        self.page = kwargs.get("page", 1)
        self.module = CouponsModule()

    def get(self):
        title = "Coupon Management Panel"
        page = request.args.get(get_page_parameter(), type=int, default=1)
        search = False
        q = request.args.get('q')
        if q:
            search = True

        pagination, coupons = self.module.search(page=page, per_page=self.per_page, search=search)
        context = locals()
        return render_template("coupons/index.html", **context)

    def post(self):
        pass

class CouponView(AuthorizedView):
    """View for an individual Coupon
    """
    def __init__(self, **kwargs):
        super().__init__()
        self.module = CouponsModule()

    def get(self, **kwargs):
        id = kwargs.get('id')
        title = "Check the WordAI Results."
        coupon = self.module.get(id)
        context = locals()
        return render_template("coupons/show.html", **context)

    def post(self):
        pass

