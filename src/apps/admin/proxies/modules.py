from src.models import Proxy, db, session

class ProxiesModule(object):
    """Proxies Module
    """
    def __init__(self):
        pass

    def get_all(self):
        return Proxy.query.all()

    def import_from_service(self, rows, source='myprivatevpn'):
        for row in rows:
            ip = row.get('proxy_ip')
            port = row.get('proxy_port')
            proxy = Proxy(name="{0}:{1}".format(ip, port), source=source)
            session.add(proxy)
        
        try:
            session.commit()
            return True
        except Exception as e:
            print(str(e))
            session.rollback()
            return False
