"""Define commands to run the server and migration."""

import os

from flask_script import Manager
from flask import redirect
from flask_migrate import Migrate, MigrateCommand

from flasgger import Swagger

from app import create_app
from app.models import db


app = create_app(config_object=os.getenv('APP_SETTINGS'))
migrate = Migrate(app, db)
manager = Manager(app)
swagger = Swagger(app)

manager.add_command('db', MigrateCommand)


@app.route('/')
def index():
    """Application homepage.
        :return
            Redirect to Application API documentation
    """
    return redirect('/apidocs')


@manager.shell
def make_shell_context():
    """Creates a python REPL"""

    return dict(app=app)


if __name__ == "__main__":
    manager.run()
