"""
Views for admin/source_app
"""

import datetime, json, requests

from flask import request, render_template, url_for, redirect, jsonify

from src.libs import AuthorizedView
from .modules import StoresModule
from .seeds import stores

class StoresView(AuthorizedView):
    """
    View for dashboard
    """
    def __init__(self):
        super().__init__()
        self.module = StoresModule()

    def get(self):
        title = "Store Management Panel"
        (stores, tasks) = self.module.get_all()
        context = locals()
        # return jsonify(tasks)
        return render_template("stores/index.html", **context)

    def post(self):
        result = self.module.refresh_stores(stores)
        return redirect(url_for('stores.index'))

class StoreView(AuthorizedView):
    """View for an individual Role
    """
    def __init__(self):
        super().__init__()
        pass

    def get(self):
        pass

    def post(self):
        pass

