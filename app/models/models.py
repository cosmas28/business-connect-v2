"""Demonstrate all user authentication functionalities.

This module provides methods that will enhance the authentication operations
such as user registration, user login, logout, reset password.

"""

import os

# from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
import jwt
from flask import current_app

from werkzeug.security import generate_password_hash, check_password_hash
from . import db
# db = SQLAlchemy()


class User(db.Model):
    """Create users table."""

    __tablename__ = 'users'
    uid = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(60))
    username = db.Column(db.String(60))
    first_name = db.Column(db.String(60))
    last_name = db.Column(db.String(60))
    pwd_hash = db.Column(db.String(120))
    businesses = db.relationship(
        'Business', order_by='Business.bid', cascade="all, delete-orphan")
    _reviews = db.relationship(
        'Reviews', order_by='Reviews.rid', cascade="all, delete-orphan")

    def __init__(self, email, username, first_name, last_name, password):
        self.email = email.lower()
        self.username = username.lower()
        self.first_name = first_name.capitalize()
        self.last_name = last_name.capitalize()
        self.set_password(password)

    def set_password(self, password):
        self.pwd_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.pwd_hash, password)

    def generate_token(self, user_id):
        """Generate access token."""

        try:
            payload = {
                'exp': datetime.utcnow() + timedelta(minutes=5),
                'iat': datetime.utcnow(),
                'sub': user_id
            }
            jwt_string = jwt.encode(
                payload, current_app.config.get('SECRET_KEY'), algorithm='HS256'
            )
            return jwt_string

        except Exception as e:
            return str(e)

    @staticmethod
    def decode_token(token):
        """Decode the access token from the Authorization header."""

        try:
            payload = jwt.decode(token, current_app.config.get('SECRET_KEY'))

            return payload['sub']
        except jwt.ExpiredSignatureError:

            return "The token is expired. Please login!"
        except jwt.InvalidTokenError:

            return "Invalid token. Please login!"


class RevokedToken(db.Model):
    """Create revoked_tokens table."""

    __tablename__ = 'revoked_tokens'
    tid = db.Column(db.Integer, primary_key=True)
    jti = db.Column(db.String(120))

    def __init__(self, jti):
        self.jti = jti

    @classmethod
    def is_jti_blacklisted(cls, jti):
        """Check if token was blacklisted.
        Args:
            jti(str): A unique identifier of the token.

        Returns:
            Boolean value.
        """

        query = cls.query.filter_by(jti=jti).first()
        return bool(query)


class Business(db.Model):
    """Create business table."""

    __tablename__ = 'business'

    bid = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60))
    category = db.Column(db.String(40))
    location = db.Column(db.String(40))
    summary = db.Column(db.Text)
    created_by = db.Column(db.Integer, db.ForeignKey(User.uid))
    _reviews = db.relationship(
        'Reviews', order_by='Reviews.rid', cascade="all, delete-orphan")

    def __init__(self, name, category, location, summary, created_by):
        self.name = name
        self.category = category
        self.location = location
        self.summary = summary
        self.created_by = created_by


class Reviews(db.Model):
    """Create reviews table."""

    __tablename__ = 'reviews'

    rid = db.Column(db.Integer, primary_key=True)
    review = db.Column(db.Text)
    review_for = db.Column(db.Integer, db.ForeignKey(Business.bid))
    reviewed_by = db.Column(db.Integer, db.ForeignKey(User.uid))

    def __init__(self, review, review_for, reviewed_by):
        self.review = review
        self.review_for = review_for
        self.reviewed_by = reviewed_by

# class User(object):
#
#     """Illustrate methods to enable user authentication.
#
#     Attributes:
#         registered_users (list): A list of dictionaries which store user records.
#
#     """
#
#     def __init__(self):
#         self.registered_users = []
#         self.user_persistent = {}
#
#     def username_exist(self, username):
#         """Check is a username exist.
#
#         Args:
#             username (str): username parameter should be unique to identify each user.
#
#         Returns:
#            boolean value
#
#         """
#         global username_exist
#         username_exist = False
#         for user in self.registered_users:
#             if user['username'] == username:
#                 username_exist = True
#
#         return username_exist
#
#     def register_user(self, username, password, confirm_password):
#         """Register a new user.
#
#         Args:
#             username (str): username parameter should be unique to identify each user.
#             password (str): password parameter should be at least 6 characters.
#             confirm_password (str): confirmation password parameter should match.
#
#         Returns:
#             A list of values of the registered username.
#             A success message when the user have been registered
#
#         """
#
#         user_data = {
#             'username': username,
#             'password': password,
#         }
#         response = ''
#
#         if self.username_exist(username):
#             response += 'The username already exist'
#         elif len(username) == 0 and len(password) == 0:
#             response += 'Username and password is required!'
#         elif len(username) == 0 or len(confirm_password) == 0:
#             response += 'Both username and password is required!'
#         elif len(password) < 6:
#             response += 'Password must be more than 6 characters!'
#         elif password != confirm_password:
#             response += 'The password does not match!'
#         else:
#             self.registered_users.append(user_data)
#
#         if self.registered_users[-1]['password'] == password:
#             response += 'Successful registered'
#
#         return response
#
#     def is_user_logged_in(self, username):
#         """Login a user.
#
#         Args:
#             username (str): username parameter should be unique to identify each user.
#
#         Returns:
#             True if the username exist in persistent data
#
#         """
#         is_logged_in = False
#         if username in self.user_persistent:
#             is_logged_in = True
#
#         return is_logged_in
#
#     def login_user(self, username, password):
#         """Login a user.
#
#         Args:
#             username (str): username parameter should be unique to identify each user.
#             password (str): password parameter should be at least 6 characters.
#
#         Returns:
#             Successful login
#
#         """
#
#         response = ''
#
#         global valid_password
#         valid_password = False
#         for user in self.registered_users:
#             if user['username'] == username and user['password'] == password:
#                 valid_password = True
#
#         if len(username) == 0 and len(password) == 0:
#             response += 'Username and password is required!'
#         elif len(username) == 0 or len(password) == 0:
#             response += 'Both username and password is required!'
#         elif not self.username_exist(username):
#             response += 'The username does not exist'
#         elif self.is_user_logged_in(username):
#             response += 'You are already logged in!'
#         elif not valid_password:
#             response += 'The password is invalid!'
#         else:
#             self.user_persistent[username] = password
#             response += 'Successful login'
#
#         return response
#
#     def logout_user(self, username):
#         """Login a user.
#
#         Args:
#             username (str): username parameter should be unique to identify each user.
#
#         Returns:
#             Success message
#
#         """
#
#         response = ''
#         if username not in self.user_persistent:
#             response += 'You are already logged out.Please login!'
#         elif username in self.user_persistent:
#             del self.user_persistent[username]
#             response += 'Logged out successfully!'
#
#         return response
#
#     def reset_password(self, username, password):
#         """Reset use password.
#
#         Args:
#             username (str): username parameter should be unique to identify each user.
#             password (str): password parameter should be at least 6 characters.
#
#         Returns:
#             Success message if the password was changed
#             Error message if the username does not exist
#
#         """
#
#         response = ''
#         if not self.username_exist(username):
#             response += 'Invalid username!'
#         elif len(password) < 6:
#             response += 'Password must be more than 6 characters!'
#         else:
#             for user in self.registered_users:
#                 if user['username'] == username:
#                     user['password'] = password
#                     response += 'Successful reset password. Login with new password!'
#
#         return response
