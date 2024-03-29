"""
Initializing routes for Admin/Roles app
"""

from .views import RolesView

def init_routes(app):
    app.add_url_rule('/', view_func=RolesView.as_view('index'))

if __name__ == "__main__":
    print("Something went wrong...")
