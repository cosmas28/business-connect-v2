"""Demonstrate all user authentication API endpoints.

This module provides API endpoints to register users,
 login users, and reset user passwords.

"""

from flask import Blueprint, request, make_response, jsonify
from flask_jwt_extended import (
    create_access_token, create_refresh_token, jwt_required,
    jwt_refresh_token_required, get_jwt_identity, get_raw_jwt
)
from flask_restful import (Resource, Api)
from werkzeug.security import generate_password_hash

from app.models import User, RevokedToken
from app.models import db
from app.helper_functions import email_exist, username_exist, valid_password


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
        first_name = req_data.get('first_name')
        last_name = req_data.get('last_name')
        password = req_data.get('password')
        confirm_password = req_data.get('confirm_password')

        not_valid_password = valid_password(password, confirm_password)
        registered = username_exist(username) or email_exist(email)
        if not email or not username:
            response_message = {'message': 'Email and Username are required!'}
            return make_response(jsonify(response_message))
        elif not password or not confirm_password:
            response_message = {
                'message': 'Password and Confirmation password are required!'
            }
            return make_response(jsonify(response_message))
        elif not_valid_password:
            return make_response(jsonify(not_valid_password))
        if not registered:
            try:
                user = User(email=email, username=username,
                            first_name=first_name, last_name=last_name,
                            password=password)
                user.save()
                response_message = {
                    'message': 'You have successfully created an account!'
                }

                return make_response(jsonify(response_message))
            except Exception as error:
                response_message = {'message': str(error)}
                return make_response(jsonify(response_message))
        else:
            response_message = {'message': 'User already exists. Sign in!'}
            return make_response(jsonify(response_message))


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

        if not email_exist(email):
            response = {
                'response_message': 'Invalid email!',
                'status_code': 401
            }
            return make_response(jsonify(response))

        user = User.query.filter_by(email=email).first()
        if email_exist(email) and user.check_password(password):
            try:
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
            except Exception as error:
                response = {
                    'response_message': str(error)
                }

                return make_response(jsonify(response))
        response = {
            'response_message': 'Invalid email or password!',
            'status_code': 401
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
            revoked_token.save()
            response = {
                'response_message': 'Log out has been successful!',
                'status_code': 200
            }
            return make_response(jsonify(response))
        except Exception as error:
            response = {
                'response_message': str(error),
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
            revoked_token.save()
            response = {
                'response_message': 'Log out has been successful!',
                'status_code': 200
            }
            return make_response(jsonify(response))
        except Exception as error:
            response = {
                'response_message': str(error),
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

        not_valid_password = valid_password(password, confirm_password)
        if not email:
            response_message = {'response_message': 'Email is required!'}
            return make_response(jsonify(response_message))
        elif not password or not confirm_password:
            response_message = {'response_message': 'Password is required!'}
            return make_response(jsonify(response_message))
        elif not_valid_password:
            return make_response(jsonify(not_valid_password))
        if email_exist(email):
            try:
                User.query.filter_by(email=email).update(dict(
                    password=generate_password_hash(password)))
                db.session.commit()

                response = {
                    'response_message': 'Password reset successfully!',
                    'status_code': 200
                }
                return make_response(jsonify(response))
            except Exception as error:
                response_message = {'message': str(error)}
                return make_response(jsonify(response_message))
        else:
            response_message = {'response_message': 'Email not registered'}
            return make_response(jsonify(response_message))


user_api = Blueprint('views.user', __name__)
api = Api(user_api)
api.add_resource(RegisterUser, '/register', endpoint='register')
api.add_resource(LoginUser, '/login', endpoint='login')
api.add_resource(TokenRefresh, '/refresh_token', endpoint='refresh_token')
api.add_resource(UserLogoutAccess, '/logout', endpoint='logout')
api.add_resource(UserLogoutRefresh,
                 '/logout_refresh_token', endpoint='logout_refresh_token')
api.add_resource(ResetPassword, '/reset_password', endpoint='reset_password')
