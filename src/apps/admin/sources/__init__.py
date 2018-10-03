from flask import Blueprint
from .routes import init_routes

sources_app = Blueprint('admin.sources', __name__)
init_routes(sources_app)
