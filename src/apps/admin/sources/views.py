"""
Views for admin/source_app
"""

import datetime, json, requests

from flask import request, render_template, url_for, redirect, jsonify

from src.libs import AdminView
from .modules import SourcesModule

class SourcesView(AdminView):
    """
    View for dashboard
    """
    def __init__(self):
        super().__init__()
        self.module = SourcesModule()

    def get(self):
        title = "Source Management Panel"
        sources = self.module.get_all()
        context = locals()
        return render_template("admin/sources/index.html", **context)

    def post(self):
        return jsonify({"status": True})

class SourceView(AdminView):
    """View for an individual Role
    """
    def __init__(self):
        super().__init__()
        pass

    def get(self):
        pass

    def post(self):
        pass

