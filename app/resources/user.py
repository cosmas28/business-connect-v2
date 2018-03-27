"""Demonstrate all user authentication API endpoints.

This module provides API endpoints to register users, login users, and reset user passwords.

"""

from flask import Blueprint,  request, make_response, jsonify
from werkzeug.security import generate_password_hash
from flask_restful import (Resource, Api, reqparse)
from flask_jwt_extended import (
    create_access_token, create_refresh_token, jwt_required, jwt_refresh_token_required, get_jwt_identity, get_raw_jwt
)

from app.models.user import User, RevokedToken
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

    """Illustrate API endpoints to register user.

    Attributes:
        reqparse (object): A request parsing interface designed to access simple and uniform
        variables on the flask.request object.

    """

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('email',
                                   required=True,
                                   help="Email is required!",
                                   location=['form', 'json']
                                   )
        self.reqparse.add_argument('username',
                                   required=True,
                                   help="Username is required!",
                                   location=['form', 'json']
                                   )
        self.reqparse.add_argument('first_name',
                                   required=True,
                                   help="First name is required!",
                                   location=['form', 'json']
                                   )
        self.reqparse.add_argument('last_name',
                                   required=True,
                                   help="Last name is required!",
                                   location=['form', 'json']
                                   )
        self.reqparse.add_argument('password',
                                   required=True,
                                   help="Password is required!",
                                   location=['form', 'json']
                                   )
        self.reqparse.add_argument('confirm_password',
                                   required=True,
                                   help="Confirmation password is required!",
                                   location=['form', 'json']
                                   )

    def post(self):
        """Register a new user.

        Returns:
            A success message to indicate successful registration.

        Raises:
            An username error when username already exist.
            Password error when the password is too short.
            Password error if the password does not much confirmation password.
            Error message if email is empty.
            Error message if username is empty.
            Error message if first name is empty.
            Error message if last name is empty.
            Error message if password is empty.
            Error message if password confirmation is empty.

        """
        req_data = request.get_json()
        email = req_data['email']
        username = req_data['username']
        first_name = req_data['first_name']
        last_name = req_data['last_name']
        password = req_data['password']
        confirm_password = req_data['confirm_password']

        db.create_all()
        db.session.commit()

        response_text = ''

        if len(email) == 0:
            response_text += 'Email is required!'
            status_code = 406
        elif len(username) == 0:
            response_text += 'Username is required!'
            status_code = 406
        elif len(first_name) == 0:
            response_text += 'First name is required!'
            status_code = 406
        elif len(last_name) == 0:
            response_text += 'Last name is required!'
            status_code = 406
        elif len(password) == 0:
            response_text += 'Password is required!'
            status_code = 406
        elif len(confirm_password) == 0:
            response_text += 'Confirmation password is required!'
            status_code = 406
        elif email_exist(email):
            response_text += 'Email already exists. Please use a unique email!'
            status_code = 406
        elif username_exist(username):
            response_text += 'Username already exists. Please use a unique username!'
            status_code = 406
        elif len(password) <= 6:
            response_text += 'Password must be more than 6 characters!'
            status_code = 406
        elif password != confirm_password:
            response_text += 'Password does not match the confirmation password!'
            status_code = 406
        else:
            user = User(email, username, first_name, last_name, password)
            db.session.add(user)
            db.session.commit()

            response_text += 'You have successfully created an account!'
            status_code = 201

        # return Response(response_text, mimetype='test/plain', status=status_code)
        return {'response_message': response_text}, status_code


class LoginUser(Resource):

    """Illustrate API endpoints to login user.

    Attributes:
        reqparse (object): A request parsing interface designed to access simple and uniform to
        variables on the flask.request object.

    """

    def post(self):
        """Login a user.

        Returns:
            A success message to indicate successful login.

        Raises:
            An username error when username does not exist exist.
            password error when the password is invalid.

        """
        req_data = request.get_json()
        email = req_data['email']
        password = req_data['password']

        try:
            user = User.query.filter_by(email=email).first()

            if len(email) == 0 and len(password) == 0:
                response = {
                    'response_message': 'Email and password is required!'
                }
                return make_response(jsonify(response))
            elif len(email) == 0:
                response = {
                    'response_message': 'Email is required!'
                }
                return make_response(jsonify(response))
            elif len(password) == 0:
                response = {
                    'response_message': 'Password is required!'
                }
                return make_response(jsonify(response))
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
                # Generate the access token. This will be used as the authorization header
                # access_token = user.generate_token(user.uid)
                access_token = create_access_token(identity=user.uid)
                refresh_token = create_refresh_token(identity=user.uid)
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
    """Logout a user using JWT access_token.

    Returns:
        A success message to indicate whether token has been revoked.

    Raises:
        Error: when something went wrong on the server.

    """

    @jwt_required
    def post(self):
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
    """Logout a user using JWT refresh_token.

    Returns:
        A success message to indicate whether token has been revoked.

    Raises:
        Error: when something went wrong on the server.

    """

    @jwt_refresh_token_required
    def post(self):
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

        Returns:
            A success message to indicate successful logout.
            An error message if username does not exist.
            An error message if no data is provided.
            An error message if the password is less than 6 characters.

        """
        req_data = request.get_json()
        email = req_data['email']
        password = req_data['password']
        confirm_password = req_data['confirm_password']

        try:

            if len(email) == 0 and len(password) == 0 and len(confirm_password) == 0:
                response = {
                    'response_message': 'Email and new password is required!'
                }
                return make_response(jsonify(response))
            elif len(email) == 0:
                response = {
                    'response_message': 'Email is required!'
                }
                return make_response(jsonify(response))
            elif len(password) == 0:
                response = {
                    'response_message': 'Password is required!'
                }
                return make_response(jsonify(response))
            elif len(confirm_password) == 0:
                response = {
                    'response_message': 'Password confirmation is required!'
                }
                return make_response(jsonify(response))
            elif email_exist(email) is False:
                response = {
                    'response_message': 'Email not registered',
                    'status_code': 401
                }
                return make_response(jsonify(response))
            else:
                user = User.query.filter_by(email=email).update(dict(pwd_hash=generate_password_hash(password)))
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


user_api = Blueprint('resources.user', __name__)
api = Api(user_api)
api.add_resource(
    RegisterUser,
    '/register_user',
    endpoint='register_user'
)
api.add_resource(
    LoginUser,
    '/login_user',
    endpoint='login_user'
)
api.add_resource(
    TokenRefresh,
    '/refresh_token',
    endpoint='refresh_token'
)
api.add_resource(
    UserLogoutAccess,
    '/logout_access_token',
    endpoint='logout_access_token'
)
api.add_resource(
    UserLogoutRefresh,
    '/logout_refresh_token',
    endpoint='logout_refresh_token'
)
api.add_resource(
    ResetPassword,
    '/reset_password',
    endpoint='reset_password'
)
