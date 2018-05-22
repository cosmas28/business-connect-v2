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
from app.helper_functions import (
    email_exist, username_exist, valid_password, check_key)


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
                    id: User
                    required:
                        - email
                        - username
                        - password
                        - confirm_password
                    properties:
                        email:
                            type: string
                            description: user email
                        username:
                            type: string
                            description: user username
                        password:
                            type: string
                            description: user password
                        confirm_password:
                            type: string
                            description: user confirmation password
                        first_name:
                            type: string
                            description: user first name
                        last_name:
                            type: string
                            description: user last name
        responses:
            201:
                description: You have successfully created an account!
                schema:
                    properties:
                        message:
                            type: string
            406:
                description: Invalid data, Null required parameters
                schema:
                    properties:
                        message:
                            type: string
        """

        req_data = request.get_json()
        if 'email' not in req_data:
            response_message = jsonify({
                'message': 'email key is required!',
                'status_code': 400})
            return response_message
        if 'username' not in req_data:
            response_message = jsonify({
                'message': 'username key is required!',
                'status_code': 400})
            return response_message
        if 'first_name' not in req_data:
            response_message = jsonify({
                'message': 'first_name key is required!',
                'status_code': 400})
            return response_message
        if 'last_name' not in req_data:
            response_message = jsonify({
                'message': 'last_name key is required!',
                'status_code': 400})
            return response_message
        if 'password' not in req_data:
            response_message = jsonify({
                'message': 'password key is required!',
                'status_code': 400})
            return response_message
        if 'confirm_password' not in req_data:
            response_message = jsonify({
                'message': 'confirm_password key is required!',
                'status_code': 400})
            return response_message

        email = req_data.get('email')
        username = req_data.get('username')
        first_name = req_data.get('first_name')
        last_name = req_data.get('last_name')
        password = req_data.get('password')
        confirm_password = req_data.get('confirm_password')

        not_valid_password = valid_password(password, confirm_password)
        registered = username_exist(username) or email_exist(email)
        if email is None and username is None:
            response_message = jsonify({
                'message': 'Email and Username are required!',
                'status_code': 406})
            return response_message
        elif not password or not confirm_password:
            response_message = jsonify({
                'message': 'Password and Confirmation password are required!',
                'status_code': 406
            })
            return response_message
        elif not_valid_password:
            response_message = jsonify(not_valid_password)
            response_message.status_code = 406
            return response_message
        if not registered:
            try:
                user = User(email=email, username=username,
                            first_name=first_name, last_name=last_name,
                            password=password)
                user.save()
                response_message = jsonify({
                    'message': 'You have successfully created an account!',
                    'status_code': 201
                })
                return response_message
            except Exception as error:
                response_message = {'message': str(error)}
                return make_response(jsonify(response_message))
        else:
            response_message = jsonify({
                'message': 'User already exists. Sign in!',
                'status_code': 406})
            return response_message


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
                    required:
                        - email
                        - password
                    properties:
                        email:
                            type: string
                            description: user email
                        password:
                            type: string
                            description: user password
        responses:
            200:
                description: Successful login
                schema:
                    properties:
                        access_token:
                            type: string
                        refresh_token:
                            type: string
                        user_id:
                            type: integer
                        response_message:
                            type: string
            401:
                description: Invalid login credentials
                schema:
                    properties:
                        response_message:
                            type: string

        """
        req_data = request.get_json()
        if 'email' not in req_data:
            response_message = jsonify({
                'message': 'email key is required!',
                'status_code': 400})
            return response_message
        if 'password' not in req_data:
            response_message = jsonify({
                'message': 'password key is required!',
                'status_code': 400})
            return response_message
        email = req_data.get('email')
        password = req_data.get('password')

        if not email_exist(email):
            response = jsonify({
                'response_message': 'Invalid email!',
                'status_code': 401
            })
            return response

        user = User.query.filter_by(email=email).first()
        if email_exist(email) and user.check_password(password):
            try:
                access_token = create_access_token(identity=user.id)
                if access_token:
                    response = jsonify({
                        'response_message': 'You logged in successfully!',
                        'access_token': access_token,
                        'user_id': user.id,
                        'status_code': 200
                    })
                    return response
            except Exception as error:
                response = {
                    'response_message': str(error)
                }

                return make_response(jsonify(response))
        response = jsonify({
            'response_message': 'Invalid email or password!',
            'status_code': 401
        })
        return response


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
                description: logout successfully
        """
        jti = get_raw_jwt()['jti']

        try:
            revoked_token = RevokedToken(jti)
            revoked_token.save()
            response = jsonify({
                'response_message': 'Log out has been successful!',
                'status_code': 200
            })
            return response
        except Exception as error:
            response = jsonify({
                'response_message': str(error),
                'status_code': 500
            })
            return response


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
            500:
                description: Internal server error
        """
        jti = get_raw_jwt()['jti']

        try:
            revoked_token = RevokedToken(jti)
            revoked_token.save()
            response = jsonify({
                'response_message': 'Log out has been successful!',
                'status_code': 200
            })
            return response
        except Exception as error:
            response = jsonify({
                'response_message': str(error),
                'status_code': 500
            })
            return response


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
                schema:
                    properties:
                        access_token:
                            type: string
        """

        current_user = get_jwt_identity()
        access_token = create_refresh_token(identity=current_user)

        response = jsonify({
            'access_token': access_token,
            'status_code': 200
        })
        return response


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
                    required:
                        - email
                        - password
                        - confirm_password
                    properties:
                        email:
                            type: string
                            description: user email
                        password:
                            type: string
                            description: user password
                        confirm_password:
                            type: string
                            description: user password confirmation
        responses:
            200:
                description: Password reset successfully
                schema:
                    properties:
                        response_message:
                            type: string
            406:
                description: Invalid data, Null required parameters
                schema:
                    properties:
                        response_message:
                            type: string
        """
        req_data = request.get_json()
        
        email = req_data.get('email')
        password = req_data.get('password')
        confirm_password = req_data.get('confirm_password')

        not_valid_password = valid_password(password, confirm_password)
        if not email:
            response_message = jsonify({
                'response_message': 'Email is required!',
                'status_code': 406})
            return response_message
        elif not password or not confirm_password:
            response_message = jsonify({
                'response_message': 'Password is required!',
                'status_code': 406})
            return response_message
        elif not_valid_password:
            response_message = jsonify(not_valid_password)
            response_message.status_code = 406
            return response_message
        if email_exist(email):
            try:
                User.query.filter_by(email=email).update(dict(
                    password=generate_password_hash(password)))
                db.session.commit()

                response = jsonify({
                    'response_message': 'Password reset successfully!',
                    'status_code': 200
                })
                return response
            except Exception as error:
                response_message = jsonify({
                    'message': str(error),
                    'status_code': 500})
                return response_message
        else:
            response_message = jsonify({
                'response_message': 'Email not registered',
                'status_code': 406})
            return response_message


user_api = Blueprint('users.views', __name__)
api = Api(user_api)
api.add_resource(RegisterUser, '/register', endpoint='register')
api.add_resource(LoginUser, '/login', endpoint='login')
api.add_resource(TokenRefresh, '/refresh_token', endpoint='refresh_token')
api.add_resource(UserLogoutAccess, '/logout', endpoint='logout')
api.add_resource(UserLogoutRefresh,
                 '/logout_refresh_token', endpoint='logout_refresh_token')
api.add_resource(ResetPassword, '/reset_password', endpoint='reset_password')
