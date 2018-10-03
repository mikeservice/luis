from flask import Blueprint
from .routes import init_routes

coupons_app = Blueprint('coupons', __name__)
init_routes(coupons_app)
