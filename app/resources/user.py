"""Demonstrate all user authentication API endpoints.

This module provides API endpoints to register users, login users, and reset user passwords.

"""

from flask import Blueprint,  request

from flask.ext.restful import (Resource, Api, reqparse)

from app.models.user import User

user = User()


class RegisterUser(Resource):

    """Illustrate API endpoints to register user.

    Attributes:
        reqparse (object): A request parsing interface designed to access simple and uniform
        variables on the flask.request object.

    """

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('username',
                                   required=True,
                                   help="Username is required!",
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
            password error when the password is too short.

        """
        req_data = request.get_json()
        username = req_data['username']
        password = req_data['password']
        confirm_password = req_data['confirm_password']

        save_response = user.register_user(username, password, confirm_password)

        return save_response, 201


class LoginUser(Resource):

    """Illustrate API endpoints to login user.

    Attributes:
        reqparse (object): A request parsing interface designed to access simple and uniform to
        variables on the flask.request object.

    """

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('username',
                                   required=True,
                                   help='Username is required!',
                                   location=['form', 'json']
                                   )
        self.reqparse.add_argument('password',
                                   required=True,
                                   help='Password is required!',
                                   location=['form', 'json']
                                   )

    def post(self):
        """Login a user.

        Returns:
            A success message to indicate successful login.

        Raises:
            An username error when username does not exist exist.
            password error when the password is invalid.

        """
        req_data = request.get_json()
        username = req_data['username']
        password = req_data['password']

        save_response = user.login_user(username, password)

        return save_response, 200


class Logout(Resource):

    """Illustrate API endpoints to logout user.

    Attributes:
        reqparse (object): A request parsing interface designed to access simple and uniform to
        variables on the flask.request object.

    """

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('username',
                                   required=True,
                                   help='Username is required!',
                                   location=['form', 'json']
                                   )

    def post(self):
        """logout a user.

        Returns:
            A success message to indicate successful logout.
            A message when the user is not logged in.

        """
        req_data = request.get_json()
        username = req_data['username']

        save_response = user.logout_user(username)

        return save_response, 200


class ResetPassword(Resource):

    """Illustrate API endpoint to reset user password.

    Attributes:
        reqparse (object): A request parsing interface designed to access simple and uniform to
        variables on the flask.request object.

    """

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('username',
                                   required=True,
                                   help='Username is required!',
                                   location=['form', 'json']
                                   )
        self.reqparse.add_argument('password',
                                   required=True,
                                   help='Password is required!',
                                   location=['form', 'json']
                                   )

    def post(self):
        """Reset user password.

        Returns:
            A success message to indicate successful logout.
            An error message if username does not exist.
            An error message if the password is less than 6 characters

        """
        req_data = request.get_json()
        username = req_data['username']
        password = req_data['password']

        save_response = user.reset_password(username, password)

        return save_response, 201


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
    Logout,
    '/logout',
    endpoint='logout'
)
api.add_resource(
    ResetPassword,
    '/reset-password',
    endpoint='reset-password'
)
