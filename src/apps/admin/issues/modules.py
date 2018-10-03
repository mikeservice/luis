from src.models import Log, db, session, or_

class IssuesModule(object):
    """Issues Module
    """
    def __init__(self):
        pass

    def get_all(self):
        return Log.query.filter(or_(Log.level=='error', Log.level=='warning')).all()

