"""
Initializing routes for Admin/Roles app
"""

from .views import SourcesView

def init_routes(app):
    app.add_url_rule('/', view_func=SourcesView.as_view('index'))

if __name__ == "__main__":
    print("Something went wrong...")
