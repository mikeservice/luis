# coding: utf-8
"""
Main Module for project.
"""

import logging, os

from flask import Flask, g
from celery import Celery

from config import app_config
import celeryconfig

from flask_login import LoginManager, current_user
from flask_migrate import Migrate
from flask_bootstrap import Bootstrap
from flask_script import Manager

login_manager = LoginManager()
from .models import db, session
from .env import DEFAULT_FLASK_CONFIG

config_name = os.getenv('FLASK_CONFIG')
if not config_name:
    config_name = DEFAULT_FLASK_CONFIG
    
app = Flask(__name__, instance_relative_config = True)
app.config.from_object(app_config[config_name])

celery = Celery(__name__, backend=app_config[config_name].CELERY_RESULT_BACKEND, broker=app_config[config_name].CELERY_BROKER_URL)
celery.config_from_object(celeryconfig)

Bootstrap(app)
db.init_app(app)

login_manager.init_app(app)
login_manager.login_message = "You must be logged in to access this page."
login_manager.login_view = "auth.login"

migrate = Migrate(app, db)
manager = Manager(app)

from src.apps import auth_app, home_app, roles_app, proxies_app, sources_app, CreateAdmin, stores_app, coupons_app, issues_app
from src.tasks import tasks_app

manager.add_command("create_admin", CreateAdmin())

app.register_blueprint(auth_app)
app.register_blueprint(home_app)
app.register_blueprint(proxies_app, url_prefix='/admin/proxies')
app.register_blueprint(roles_app, url_prefix='/admin/roles')
app.register_blueprint(sources_app, url_prefix='/admin/sources')
app.register_blueprint(issues_app, url_prefix='/admin/issues')
app.register_blueprint(stores_app, url_prefix='/stores')
app.register_blueprint(coupons_app, url_prefix='/coupons')
app.register_blueprint(tasks_app, url_prefix='/tasks')

logging.basicConfig()

@app.errorhandler(500)
def server_error(e):
    logging.exception('An error occurred during a request.')
    return """
    An internal error occurred: <pre>{}</pre>
    See logs for full stacktrace.
    """.format(e), 500

@app.errorhandler(404)
def page_not_found(e):
    logging.exception("Page not found.")
    return """
    Page not found: <pre>{}</pre>
    See logs for full track.
    """.format(e), 404

@app.teardown_request
def shutdown_session(exception=None):
    db.session.remove()

@app.before_request
def before_request():
    g.user = current_user
