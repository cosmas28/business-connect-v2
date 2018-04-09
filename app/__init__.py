import os

from flask import Flask
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager

from app.resources.business import business_api
from app.resources.user import user_api
from app.resources.reviews import reviews_api

from app.models.models import RevokedToken
from app.models import db


def create_app(config_object):

    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(config_object)

    db.init_app(app)

    migrate = Migrate(app, db)

    jwt = JWTManager(app)

    @jwt.token_in_blacklist_loader
    def check_if_token_in_blacklist(decrypted_token):
        jti = decrypted_token['jti']

        return RevokedToken.is_jti_blacklisted(jti)
    from app.models import models

    app.register_blueprint(user_api, url_prefix='/api/v2/auth')
    app.register_blueprint(business_api, url_prefix='/api/v2')
    app.register_blueprint(reviews_api, url_prefix='/api/v2')

    return app
