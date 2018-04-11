"""Demonstrate all models."""

from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class User(db.Model):
    """Create users table."""

    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(60), unique=True, nullable=False)
    username = db.Column(db.String(60), unique=True, nullable=False)
    first_name = db.Column(db.String(60), nullable=True)
    last_name = db.Column(db.String(60), nullable=True)
    password = db.Column(db.String(120), nullable=False)
    businesses = db.relationship(
        'Business', order_by='Business.id', cascade='all, delete-orphan')
    _reviews = db.relationship(
        'Reviews', order_by='Reviews.id', cascade='all, delete-orphan')

    def __init__(self, email, username, first_name, last_name, _password, confirm_password):
        self.email = email.lower()
        self.username = username.lower()
        self.first_name = first_name.capitalize()
        self.last_name = last_name.capitalize()
        self.password = self.set_password(_password)
        self.confirm_password = self.set_password(confirm_password)

    def set_password(self, _password):
        return generate_password_hash(_password)

    def check_password(self, _password):
        return check_password_hash(self.password, _password)

    @staticmethod
    def valid_password(password, confirm_password):
        """Check whether the password have more than 6 characters."""

        if len(password) <= 6:
            return 'Password must be more than 6 characters!'
        elif password != confirm_password:
            return 'Password does not match the confirmation password!'
        else:
            return True

    @staticmethod
    def validate_login_data(email, password):
        """Check whether user have entered the required data to login."""

        if len(email) == 0 and len(password) == 0:
            response = {
                'response_message': 'Email and password is required!'
            }
            return response
        elif len(email) == 0:
            response = {
                'response_message': 'Email is required!'
            }
            return response
        elif len(password) == 0:
            response = {
                'response_message': 'Password is required!'
            }
            return response
        else:
            return True

    @staticmethod
    def validate_password_reset_data(email, password, confirm_password):
        """Check whether user have entered the required data to reset password."""

        if len(email) == 0 and len(password) == 0 and len(confirm_password) == 0:
            response = {
                'response_message': 'Email and new password is required!'
            }
            return response
        elif len(email) == 0:
            response = {
                'response_message': 'Email is required!'
            }
            return response
        elif len(password) == 0:
            response = {
                'response_message': 'Password is required!'
            }
            return response
        elif len(confirm_password) == 0:
            response = {
                'response_message': 'Password confirmation is required!'
            }
            return response
        else:
            return True


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

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), unique=True, nullable=False)
    category = db.Column(db.String(40), nullable=False)
    location = db.Column(db.String(40), nullable=False)
    summary = db.Column(db.Text, nullable=False)
    created_by = db.Column(db.Integer, db.ForeignKey(User.id))
    _reviews = db.relationship(
        'Reviews', order_by='Reviews.id', cascade='all, delete-orphan')

    def __init__(self, name, category, location, summary, created_by):
        self.name = name
        self.category = category
        self.location = location
        self.summary = summary
        self.created_by = created_by


class Reviews(db.Model):
    """Create reviews table."""

    __tablename__ = 'reviews'

    id = db.Column(db.Integer, primary_key=True)
    review = db.Column(db.Text, nullable=False)
    review_for = db.Column(db.Integer, db.ForeignKey(Business.id))
    reviewed_by = db.Column(db.Integer, db.ForeignKey(User.id))

    def __init__(self, review, review_for, reviewed_by):
        self.review = review
        self.review_for = review_for
        self.reviewed_by = reviewed_by
