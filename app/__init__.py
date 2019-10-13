import os
from flask import Flask, jsonify
from flask_jwt_extended import JWTManager
from flask_cors import CORS

from app.models import RevokedToken
from app.models import db
from app.business.views import business_api
from app.reviews.views import reviews_api
from app.users.views import user_api
from app.utils import mail

from config import app_config


def create_app(config_object):

    app = Flask(__name__, instance_relative_config=True)
    CORS(app)
    app.config.from_object(app_config[config_object])
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config.update(
        MAIL_SERVER='smtp.gmail.com',
        MAIL_PORT=465,
        MAIL_USE_SSL=True,
        MAIL_USERNAME=os.getenv('CONFIG_EMAIL'),
        MAIL_PASSWORD=os.getenv('CONFIG_EMAIL_PASSWORD')
    )
    mail.init_app(app)

    db.init_app(app)

    jwt = JWTManager(app)

    @app.errorhandler(404)
    def page_not_found(e):
        response = jsonify({
            'response_message': 'Page not found!',
            'status_code': 404
        })
        return response

    @jwt.token_in_blacklist_loader
    def check_if_token_in_blacklist(decrypted_token):
        jti = decrypted_token['jti']

        return RevokedToken.is_jti_blacklisted(jti)

    app.register_blueprint(user_api, url_prefix='/api/v2/auth')
    app.register_blueprint(business_api, url_prefix='/api/v2')
    app.register_blueprint(reviews_api, url_prefix='/api/v2')

    return app
