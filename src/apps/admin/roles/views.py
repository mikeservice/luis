"""
Views for home app
"""

import datetime, json
import dateutil.relativedelta

from flask import request, render_template, url_for, redirect, jsonify

from src.libs import AdminView
from .modules import RolesModule

class RolesView(AdminView):
    """
    View for dashboard
    """
    def __init__(self):
        super().__init__()
        self.module = RolesModule()

    def get(self):
        title = "Role Management Panel"
        roles = self.module.get_all()
        context = locals()
        return render_template("admin/roles/index.html", **context)

    def post(self):
        pass

class RoleView(AdminView):
    """View for an individual Role
    """
    def __init__(self):
        super().__init__()
        pass

    def get(self):
        pass

    def post(self):
        pass

