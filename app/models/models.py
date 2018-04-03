"""Demonstrate all models."""

from werkzeug.security import generate_password_hash, check_password_hash
from . import db


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
        'Business', order_by='Business.bid', cascade='all, delete-orphan')
    _reviews = db.relationship(
        'Reviews', order_by='Reviews.rid', cascade='all, delete-orphan')

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
        'Reviews', order_by='Reviews.rid', cascade='all, delete-orphan')

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
