from flask import Blueprint
from .routes import init_routes

stores_app = Blueprint('stores', __name__)
init_routes(stores_app)
