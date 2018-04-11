"""Demonstrate all user authentication API endpoints.

This module provides API endpoints to register users, login users, and reset user passwords.

"""

from flask import Blueprint, request, make_response, jsonify
from flask_jwt_extended import (
    create_access_token, create_refresh_token, jwt_required, jwt_refresh_token_required, get_jwt_identity, get_raw_jwt
)
from flask_restful import (Resource, Api)
from werkzeug.security import generate_password_hash
from sqlalchemy import exc

from app.models import User, RevokedToken
from app.models import db


def email_exist(email):
    exists = User.query.filter_by(email=email).first()

    if exists is None:
        return False
    else:
        return True


def username_exist(user_name):
    exists = User.query.filter_by(username=user_name.lower()).first()

    if exists is None:
        return False
    else:
        return True


class RegisterUser(Resource):

    """Illustrate API endpoints to register user."""

    def post(self):
        """Register a new user.
        ---
        tags:
            - User authentication and authorization
        parameters:
            -   in: body
                name: body
                schema:
                    $ref: '#/definitions/User'
        responses:
            201:
                description: OK
                content:
                    application/json:
                        schema:
                            type: object
                            properties:
                                response_message:
                                    type: string
                                    description: response message to show successful registration
        """

        req_data = request.get_json()
        email = req_data.get('email')
        username = req_data.get('username')
        password = req_data.get('password')
        confirm_password = req_data.get('confirm_password')

        db.create_all()
        db.session.commit()

        validation_res = User.valid_password(password, confirm_password)
        try:
            if validation_res is not True:
                response_text = {'response_message': validation_res}
                return response_text, 406
            elif email_exist(email):
                response_text = {'response_message': 'Email already exists. Please use a unique email!'}
                return response_text, 406
            elif username_exist(username):
                response_text = {'response_message': 'Username already exists. Please use a unique username!'}
                return response_text, 406
            else:
                user = User(email, username, '', '', password, confirm_password)
                db.session.add(user)
                db.session.commit()
                response_text = 'You have successfully created an account!'

                return {'response_message': response_text}, 201
        except exc.IntegrityError:
            response_text = 'All fields are required!'
            return {'response_message': response_text}, 406


class LoginUser(Resource):

    """Illustrate API endpoints to login user."""

    def post(self):
        """Login a user.
        ---
        tags:
            -   User authentication and authorization
        parameters:
            -   in: body
                name: body
                schema:
                    $ref: '#/definitions/User'
        responses:
            200:
                description: OK
                content:
                    application/json:
                        schema:
                            type: object
                            properties:
                                response_message:
                                    type: string
                                    description: message to show successful login
                                status_code:
                                    type: integer
                                    description: HTTP status code
                                access_token:
                                    type: string
                                    description: JSON token for user authorization
                                refresh_token:
                                    type: string
                                    description: refreshed JSON token for user authorization

        """
        req_data = request.get_json()
        email = req_data.get('email')
        password = req_data.get('password')

        try:
            user = User.query.filter_by(email=email).first()
            validation_res = User.validate_login_data(email, password)

            if validation_res is not True:
                return make_response(jsonify(validation_res))
            elif email_exist(email) is False:
                response = {
                    'response_message': 'Invalid email or password!',
                    'status_code': 401
                }
                return make_response(jsonify(response))
            elif not user.check_password(password):
                response = {
                    'response_message': 'Invalid email or password!',
                    'status_code': 401
                }
                return make_response(jsonify(response))
            else:
                access_token = create_access_token(identity=user.id)
                refresh_token = create_refresh_token(identity=user.id)
                if access_token:
                    response = {
                        'response_message': 'You logged in successfully!',
                        'status_code': 200,
                        'access_token': access_token,
                        'refresh_token': refresh_token
                    }
                    return make_response(jsonify(response))

        except Exception as e:
            response = {
                'response_message': str(e)
            }

            return make_response(jsonify(response))


class UserLogoutAccess(Resource):
    """Illustrate API endpoints to logout user using access-token."""

    @jwt_required
    def post(self):
        """Logout a user using JWT access-token.
        ---
        tags:
            - User authentication and authorization
        security:
            $ref: '#/components/securitySchemes/BearAuth'
        responses:
            200:
                description: OK
                content:
                    application/json:
                        schema:
                            type: object
                            properties:
                                response_message:
                                    type: string
                                    description: response message to show successful logout
                                status_code:
                                    type: integer
                                    description: HTTP status code
        """
        jti = get_raw_jwt()['jti']

        try:
            revoked_token = RevokedToken(jti)
            db.session.add(revoked_token)
            db.session.commit()
            response = {
                'response_message': 'Log out has been successful!',
                'status_code': 200
            }
            return make_response(jsonify(response))
        except Exception as e:
            response = {
                'response_message': str(e),
                'status_code': 500
            }
            return make_response(jsonify(response))


class UserLogoutRefresh(Resource):
    """Illustrate API endpoints to logout user using refresh-token."""

    @jwt_refresh_token_required
    def post(self):
        """Logout a user using JWT refresh_token.
        ---
        tags:
            - User authentication and authorization
        security:
            $ref: '#/components/securitySchemes/BearAuth'
        responses:
            200:
                description: Log out has been successful!
                content:
                    application/json:
                        schema:
                            type: object
                            properties:
                                response_message:
                                    type: string
                                    description: response message to show successful logout
                                status_code:
                                    type: integer
                                    description: HTTP status code
        """
        jti = get_raw_jwt()['jti']

        try:
            revoked_token = RevokedToken(jti)
            db.session.add(revoked_token)
            db.session.commit()
            response = {
                'response_message': 'Log out has been successful!',
                'status_code': 200
            }
            return make_response(jsonify(response))
        except Exception as e:
            response = {
                'response_message': str(e),
                'status_code': 500
            }
            return make_response(jsonify(response))


class TokenRefresh(Resource):
    """Reissue access token with refresh token."""

    @jwt_refresh_token_required
    def post(self):
        """refresh access-token.
        ---
        tags:
            -   User authentication and authorization
        security:
            $ref: '#/components/securitySchemes/BearAuth'
        responses:
            200:
                description: OK
                content:
                    application/json:
                        schema:
                            type: object
                            properties:
                                access_token:
                                    type: string
                                    description: JSON token for user authorization
        """

        current_user = get_jwt_identity()
        access_token = create_refresh_token(identity=current_user)

        response = {
            'access_token': access_token
        }

        return make_response(jsonify(response))


class ResetPassword(Resource):

    """Illustrate API endpoint to reset user password."""

    def post(self):
        """Reset user password.
        ---
        tags:
            - User authentication and authorization
        parameters:
            -   in: body
                name: body
                schema:
                    $ref: '#/definitions/User'
        responses:
            200:
                description: Password reset successfully
                content:
                    application/json:
                        schema:
                            type: object
                            properties:
                                response_message:
                                    type: string
                                    description: response message to show password has been reset successful
        """
        req_data = request.get_json()
        email = req_data.get('email')
        password = req_data.get('password')
        confirm_password = req_data.get('confirm_password')

        try:
            validation_res = User.validate_password_reset_data(email, password, confirm_password)
            if validation_res is not True:
                return make_response(jsonify(validation_res))
            elif email_exist(email) is False:
                response = {
                    'response_message': 'Email not registered',
                    'status_code': 401
                }
                return make_response(jsonify(response))
            else:
                user = User.query.filter_by(email=email).update(dict(password=generate_password_hash(password)))
                db.session.commit()

                response = {
                    'response_message': 'Password reset successfully!',
                    'status_code': 200
                }
                return make_response(jsonify(response))

        except Exception as e:
            response = {
                'response_message': str(e)
            }

            return make_response(jsonify(response))


user_api = Blueprint('views.user', __name__)
api = Api(user_api)
api.add_resource(RegisterUser, '/register', endpoint='register')
api.add_resource(LoginUser, '/login', endpoint='login')
api.add_resource(TokenRefresh, '/refresh_token', endpoint='refresh_token')
api.add_resource(UserLogoutAccess, '/logout', endpoint='logout')
api.add_resource(UserLogoutRefresh,'/logout_refresh_token', endpoint='logout_refresh_token')
api.add_resource(ResetPassword, '/reset_password', endpoint='reset_password')
