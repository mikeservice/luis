from flask import Blueprint, jsonify, url_for
from .routes import init_routes

tasks_app = Blueprint("tasks", __name__)

from .units import celery
init_routes(tasks_app)