from flask_script import Command

from src.models import Role, User, db, session
from .proxies import proxies_app
from .roles import roles_app
from .sources import sources_app
from .issues import issues_app


class CreateAdmin(Command):
    """ Create superuser 'admin' with 'dontfuckwithme' password """

    roles = [{
            "name" : "Administrator",
            "description" : "Super admin of system, who will have all permissions."
        }, {
            "name" : "User",
            "description" : "Default user role."
        }]

    def create_roles(self):
        for item in self.roles:
            role = Role.query.filter_by(name=item.get('name')).first()
            if role:
                print('Role <<{0}>> already exists.')
            else:
                role = Role(name=item.get('name'), description=item.get('description'))
                db.session.add(role)
                db.session.commit()
                print("Role<{0}> created.")
        

    def run(self):
        self.create_roles()
        admin = Role.query.filter_by(name=self.roles[0].get('name')).first()
        user = User.query.filter_by(username='admin').first()

        if user:
            user.password = 'dontfuckwithme'
            user.role = admin
            print('admin <<root>> exist, password changed')

        else:
            user = User(username='admin', email='leanrank@gmail.com', first_name="Lean", last_name="Rank")
            user.password = 'dontfuckwithme'
            user.role = admin
            db.session.add(user)

        db.session.commit()
        print("username:admin, password:dontfuckwithme")
