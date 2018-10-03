"""
Views for admin/proxy_app
"""

import datetime, json, requests
import dateutil.relativedelta

from flask import request, render_template, url_for, redirect, jsonify

from src.libs import AdminView
from .modules import IssuesModule

class IssuesView(AdminView):
    """
    View for dashboard
    """
    def __init__(self):
        super().__init__()
        self.module = IssuesModule()

    def get(self):
        title = "Issue Management Panel"
        issues = self.module.get_all()
        context = locals()
        return render_template("admin/issues/index.html", **context)

    def post(self):
        return "Not implemented this page."

class IssueView(AdminView):
    """View for an individual Role
    """
    def __init__(self):
        super().__init__()
        pass

    def get(self):
        pass

    def post(self):
        pass

