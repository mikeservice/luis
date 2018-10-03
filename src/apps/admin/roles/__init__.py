from flask import Blueprint
from .routes import init_routes

roles_app = Blueprint('admin.roles', __name__)
init_routes(roles_app)
