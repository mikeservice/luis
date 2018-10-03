from flask import Blueprint
from .routes import init_routes

issues_app = Blueprint('admin.issues', __name__)
init_routes(issues_app)
