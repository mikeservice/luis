"""
Views for tasks app
"""

import datetime, json
import dateutil.relativedelta

from flask import request, render_template, url_for, redirect, jsonify

from src.libs import AuthorizedView
from .modules import TasksModule
from .units import grab_coupons, check_store

class TasksView(AuthorizedView):
    """
    View for Tasks
    """
    def __init__(self):
        super().__init__()
        self.module = TasksModule()

    def get(self):
        tasks = self.module.get_all()
        context = locals()
        # return jsonify(tasks)
        return render_template("tasks/index.html", title = "Task Management", **context)

    def post(self):
        # task = grab_coupons.apply_async()
        return redirect(url_for('tasks.index'))

class TasksFeedView(AuthorizedView):
    """View for tasks live feed
    """
    def __init__(self):
        super().__init__()
        self.module = TasksModule()

    def get(self):
        tasks = self.module.get_all()
        return render_template("tasks/_tbody.html", tasks=tasks)
    
    def post(self):
        tasks = self.module.get_all()
        return render_template("tasks/_tbody.html", tasks=tasks)

class TaskView(AuthorizedView):
    """View for individual task
    """
    def __init__(self, **kwargs):
        super().__init__()
        self.id = None
        self.module = TasksModule()

    def get(self, **kwargs):
        self.id = kwargs.get('id')
        task = check_store.AsyncResult(self.id)
        if task.state == 'PENDING':
            # job did not start yet
            response = {
                'state': task.state,
                'current': 0,
                'total': 1,
                'status': 'Pending...'
            }
        elif task.state != 'FAILURE':
            response = {
                'state': task.state,
                'current': task.info.get('current', 0),
                'total': task.info.get('total', 1),
                'status': task.info.get('status', '')
            }
            if 'result' in task.info:
                response['result'] = task.info['result']
        else:
            # something went wrong in the background job
            response = {
                'state': task.state,
                'current': 1,
                'total': 1,
                'status': str(task.info),  # this is the exception raised
            }
        return jsonify(response)
    
    def post(self):
        pass

