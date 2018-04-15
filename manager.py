from flask_script import Manager, Server
from back_end import app, db
from models import Users

manager = Manager(app)
manager.add_command("server", Server())

@manager.shell
def make_shell_context():
    return dict(app=app, db=db, User=Users)