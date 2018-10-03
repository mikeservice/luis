"""
Route Configuration for Tasks
"""
from .views import TasksView, TaskView, TasksFeedView

def init_routes(app):
    app.add_url_rule('/', view_func=TasksView.as_view('index'))
    app.add_url_rule('/<id>', view_func=TaskView.as_view('detail'))
    app.add_url_rule('/feed', view_func=TasksFeedView.as_view('feed'))

if __name__ == "__main__":
    print("Something went wrong...")
