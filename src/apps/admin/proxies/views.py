"""
Views for admin/proxy_app
"""

import datetime, json, requests
import dateutil.relativedelta

from flask import request, render_template, url_for, redirect, jsonify

from src.libs import AdminView
from .modules import ProxiesModule

class ProxiesView(AdminView):
    """
    View for dashboard
    """
    def __init__(self):
        super().__init__()
        self.module = ProxiesModule()

    def get(self):
        title = "Proxy Management Panel"
        proxies = self.module.get_all()
        context = locals()
        return render_template("admin/proxies/index.html", **context)

    def post(self):
        my_private_vpn_api_url = 'https://api.myprivateproxy.net/v1/fetchProxies/json/brief/yva870v87gbt9ozq672x9pfebucqmzgz'
        r = requests.get(my_private_vpn_api_url)
        rows = r.json()
        result = self.module.import_from_service(rows)
        if result:
            return redirect(url_for('admin.proxies.index'))
        else:
            return jsonify(rows)

class ProxyView(AdminView):
    """View for an individual Role
    """
    def __init__(self):
        super().__init__()
        pass

    def get(self):
        pass

    def post(self):
        pass

