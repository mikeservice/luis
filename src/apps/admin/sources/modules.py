from src.models import Source, db, session

class SourcesModule(object):
    """Sources Module
    """
    def __init__(self):
        pass

    def get_all(self):
        return Source.query.all()

