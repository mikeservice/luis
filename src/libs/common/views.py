"""
Common Libraries to be used in system level
"""
from flask import g, request, redirect, url_for, abort
from flask.views import MethodView
from flask_login import login_required
from functools import wraps

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if g.user is None:
            return redirect(url_for('login', next=request.url))
        elif g.user.role is None or g.user.role.name != "Administrator":
            abort(401)
        return f(*args, **kwargs)
    return decorated_function

class AuthorizedView(MethodView):
    """
    Base class for authorized view.
    """
    decorators = [login_required]

    def __init__(self):
        pass

class AdminView(AuthorizedView):
    """
    Base class for super admin view
    """
    decorators = [admin_required]

    def __init__(self):
        pass

