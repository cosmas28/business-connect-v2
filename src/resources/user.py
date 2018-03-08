"""Demonstrate all user authentication API endpoints.

This module provides API endpoints to register users, login users, and reset user passwords.

"""

from flask import Blueprint, abort, request

from flask.ext.restful import (Resource, Api, reqparse)

from src.models.user import User

user = User()


class RegisterUser(Resource):

    """Illustrate methods to manipulate business data.

    Attributes:
        reqparse (object): A request parsing interface designed to access simple and uniform to
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

    def post(self):
        """Register a new business.

        Args:
            username (str): username is a unique field to identify user.
            password (str): secret word to authenticate users.

        Returns:
            A success message to indicate successful registration.

        Raises:
            An username error when username already exist.
            password error when the password is too short.

        """
        req_data = request.get_json()
        username = req_data["username"]
        password = req_data["password"]

        save_response = user.register_user(username, password)

        return save_response, 201


user_api = Blueprint('resources.user', __name__)
api = Api(user_api)
api.add_resource(
    RegisterUser,
    '/register_user',
    endpoint='register_user'
)