from flask import Blueprint
from .routes import init_routes

proxies_app = Blueprint('admin.proxies', __name__)
init_routes(proxies_app)
