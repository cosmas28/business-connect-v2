"""Design test case to test business related functionalities.

This module design test suite in which contains test cases for behaviors that
are expected from business model.

"""


import unittest

from app.models import User, Business, Reviews, RevokedToken
from app.models import db
from . import app


class ModelsTestCase(unittest.TestCase):

    """Illustrate test cases to test expected behavior of add reviews functionality. """

    def setUp(self):
        """Call this before every test."""

        db.app = app
        db.create_all()

    def tearDown(self):
        """Call after every test to remove the created table."""

        db.session.remove()
        db.drop_all()

    def test_user_model_can_register_users(self):
        """Test whether user model can register users."""

        user = User('test@andela.com', 'testuser', 'first', 'last', 'password')
        db.session.add(user)
        db.session.commit()
        self.assertEqual(User.query.count(), 1)

    def test_user_password(self):
        """Test whether user password matches hashed password."""

        user = User('test@andela.com', 'testuser', 'first', 'last', 'password')
        db.session.add(user)
        db.session.commit()

        self.assertTrue(user.check_password('password'))

    def test_revoked_token_model(self):
        """Test whether RevokedTokenModel instance works."""

        revoked_token = RevokedToken('secret_token')
        db.session.add(revoked_token)
        db.session.commit()

        query_res = RevokedToken.query.filter_by(jti='secret_token').first()

        self.assertTrue(query_res)

    def test_token_was_blacklisted(self):
        """Test whether revoked token exists."""

        revoked_token = RevokedToken('secret_token_blacklisted')
        db.session.add(revoked_token)
        db.session.commit()

        self.assertTrue(RevokedToken.is_jti_blacklisted('secret_token_blacklisted'))

    def test_business_model(self):
        """Test whether business model is working."""

        user = User('test@andela.com', 'testuser', 'first', 'last', 'password')
        db.session.add(user)
        db.session.commit()
        query_user = User.query.filter_by(email='test@andela.com').first()

        business = Business('CosmasTech', 'Technology', 'Nairobi', 'AI is transforming human life', query_user.uid)
        db.session.add(business)
        db.session.commit()

        query_res = Business.query.filter_by(bid=1).first()
        self.assertEqual(query_res.name, 'CosmasTech')

    def test_reviews_model(self):
        """Test whether review model is working."""

        user = User('test@andela.com', 'testuser', 'first', 'last', 'password')
        db.session.add(user)
        db.session.commit()
        query_user = User.query.filter_by(email='test@andela.com').first()

        business = Business('CosmasTech', 'Technology', 'Nairobi', 'AI is transforming human life', query_user.uid)
        db.session.add(business)
        db.session.commit()
        query_business = Business.query.filter_by(name='CosmasTech').first()

        business = Reviews('The business will really save the world!', query_business.bid, query_user.uid)
        db.session.add(business)
        db.session.commit()
        query_reviews = Reviews.query.filter_by(rid=1).first()

        self.assertEqual(query_reviews.review, 'The business will really save the world!')


if __name__ == '__main__':
    unittest.main()
