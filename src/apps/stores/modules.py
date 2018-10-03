from urllib.parse import urlparse
from src.models import Source, Store, db, session
from flask_login import current_user
from src.tasks.units import check_store

class StoresModule(object):
    """Stores Module
    """
    def __init__(self):
        pass

    def get_all(self):
        stores = Store.query.all()
        tasks = dict()

        for store in stores:
            if store.job_uid:
                task = check_store.AsyncResult(store.job_uid)
                tasks[store.job_uid] = {"status": task.state}
        
        return (stores, tasks)
    
    def refresh_stores(self, rows):
        stores = list()
        for (store_name, url) in rows:
            parsed_url = urlparse(url)
            store_name = store_name.lower()
            base_url = "{0}://{1}".format(parsed_url.scheme, parsed_url.hostname)
            start_point = parsed_url.path
            source_name = parsed_url.hostname.split(".")[-2].lower()
            source = Source.query.filter(Source.name==source_name).first()
            if not source:
                source = Source(name=source_name)
                source.created_by = current_user.id
                source.updated_by = current_user.id
                session.add(source)
            
            source.base_url = base_url
            try:
                session.commit()
            except Exception as e:
                session.rollback()
                print(str(e))
                return False
            
            store = Store.query.filter(Store.name==store_name, Store.source==source).first()
            if not store:
                store = Store(name=store_name, source_id=source.id)
                session.add(store)
            
            store.start_point = start_point
            try:
                session.commit()
            except Exception as e:
                session.rollback()
                print(str(e))
                return False
        
        return True

