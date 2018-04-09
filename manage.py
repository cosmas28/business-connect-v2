from flask_script import Manager
from flask_migrate import MigrateCommand

from flasgger import Swagger

from app import create_app


app = create_app('config.DevelopmentConfig')
manager = Manager(app)
swagger = Swagger(app)

manager.add_command('db', MigrateCommand)

@manager.shell
def make_shell_context():
    """Creates a python REPL"""

    return dict(app=app)

if __name__ == "__main__":
    manager.run()
