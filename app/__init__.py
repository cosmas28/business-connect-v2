import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

# from app.resources.business import business_api
# from app.resources.user import user_api
# from app.resources.reviews import reviews_api

from config import config

db = SQLAlchemy()


def create_app():
    if os.environ.get('FLASK_CONFIG') == 'production':
        app = Flask(__name__)
        app.config.update(
            SECRET_KEY=os.environ.get('SECRET_KEY'),
            SQLALCHEMY_DATABASE_URI=os.environ.get('SQLALCHEMY_DATABASE_URI')
        )
    else:
        app = Flask(__name__, instance_relative_config=True)
        app.config.from_object(config['development'])
        app.config.from_pyfile('config.py')

    db.init_app(app)

    migrate = Migrate(app, db)

    manager = Manager(app)
    manager.add_command('db', MigrateCommand)

    from app.models import user

    # app.register_blueprint(business_api, url_prefix='/api/v1')
    # app.register_blueprint(user_api, url_prefix='/api/v1')
    # app.register_blueprint(reviews_api, url_prefix='/api/v1')

    return manager
