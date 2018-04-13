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

    def __init__(self, email, username, first_name, last_name, password):
        self.email = email.lower()
        self.username = username.lower()
        self.first_name = first_name.capitalize()
        self.last_name = last_name.capitalize()
        self.password = self.set_password(password)

    def set_password(self, password):
        return generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def save(self):
        db.session.add(self)
        db.session.commit()


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

    def save(self):
        db.session.add(self)
        db.session.commit()


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

    def save(self):
        db.session.add(self)
        db.session.commit()


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
