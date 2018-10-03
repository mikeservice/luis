from src.models import Role

class RolesModule(object):
    """Roles Module
    """
    def __init__(self):
        pass

    def get_all(self):
        return Role.query.all()
