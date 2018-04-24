from flask import Flask
from flask_jwt_extended import JWTManager
from flask_cors import CORS

from app.models import RevokedToken
from app.models import db
from app.views.business import business_api
from app.views.reviews import reviews_api
from app.views.user import user_api

from config import app_config


def init_heroku(app):
    app.config.update(
        SQLALCHEMY_DATABASE_URI=os.environ['DATABASE_URL']
    )


def create_app(config_object):

    app = Flask(__name__, instance_relative_config=True)
    CORS(app)
    app.config.from_object(app_config[config_object])
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    init_heroku(app)

    db.init_app(app)

    jwt = JWTManager(app)

    @jwt.token_in_blacklist_loader
    def check_if_token_in_blacklist(decrypted_token):
        jti = decrypted_token['jti']

        return RevokedToken.is_jti_blacklisted(jti)

    app.register_blueprint(user_api, url_prefix='/api/v2/auth')
    app.register_blueprint(business_api, url_prefix='/api/v2')
    app.register_blueprint(reviews_api, url_prefix='/api/v2')

    return app
