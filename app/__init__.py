import os

from flask import Flask
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager

from app.resources.business import business_api
from app.resources.user import user_api
from app.resources.reviews import reviews_api

from app.models.user import RevokedToken
from app.models import db


def create_app(config_object):
    if os.environ.get('FLASK_CONFIG') == 'production':
        app = Flask(__name__)
        app.config.update(
            SECRET_KEY=os.environ.get('SECRET_KEY'),
            SQLALCHEMY_DATABASE_URI=os.environ.get('SQLALCHEMY_DATABASE_URI')
        )
    else:
        app = Flask(__name__, instance_relative_config=True)
        app.config.from_object(config_object)
        app.config.from_pyfile('config.py')

    db.init_app(app)

    migrate = Migrate(app, db)

    jwt = JWTManager(app)

    @jwt.token_in_blacklist_loader
    def check_if_token_in_blacklist(decrypted_token):
        jti = decrypted_token['jti']

        return RevokedToken.is_jti_blacklisted(jti)
    from app.models import user

    app.register_blueprint(user_api, url_prefix='/api/v1/auth')
    app.register_blueprint(business_api, url_prefix='/api/v1')
    app.register_blueprint(reviews_api, url_prefix='/api/v1')

    return app
