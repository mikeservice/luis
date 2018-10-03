from src.models import Store
from src.tasks.units import check_store

class TasksModule(object):
    """
    Dashboar Module
    """
    def __init__(self):
        pass

    def get_all(self, *args, **kwargs):
        tasks = list()
        for store in Store.query.filter(Store.job_uid!=None).all():
            task = check_store.AsyncResult(store.job_uid)
            
            if not task or not task.info:
                continue
            state = task.info
            tasks.append({
                "store": store.as_dict,
                "progress": int(state.get('current', 0) / state.get('total', 1) * 100) if type(state).__name__ == 'dict' else 'error',
                "msg": state.get('status') if type(state).__name__ == 'dict' else 'error'
            })
        
        return tasks

    def post(self, *args, **kwargs):
        pass

