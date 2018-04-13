"""Design test case to test business related functionalities.

This module design test suite in which contains test cases for behaviors that
are expected from business model.

"""


import unittest

from app.models import User, Business, Reviews, RevokedToken
from app.models import db
from . import app


class ModelsTestCase(unittest.TestCase):

    """
        Illustrate test cases to test expected behavior
        of add reviews functionality.
     """

    def setUp(self):
        """Call this before every test."""

        db.app = app
        db.create_all()

        self.user = User('test@andela.com', 'testuser',
                         'first', 'last', 'password')

    def tearDown(self):
        """Call after every test to remove the created table."""

        db.session.remove()
        db.drop_all()

    def test_user_model(self):
        """Test whether user model can register users."""

        self.user.save()
        self.assertEqual(User.query.count(), 1)

    def test_check_password_method(self):
        """Test whether user password matches hashed password."""

        self.user.save()

        self.assertTrue(self.user.check_password('password'))

    def test_revoked_token_model(self):
        """Test whether RevokedTokenModel instance works."""

        revoked_token = RevokedToken('secret_token')
        revoked_token.save()

        query_res = RevokedToken.query.filter_by(jti='secret_token').first()

        self.assertTrue(query_res)

    def test_token_was_blacklisted(self):
        """Test whether revoked token exists."""

        revoked_token = RevokedToken('secret_token_blacklisted')
        revoked_token.save()

        self.assertTrue(
            RevokedToken.is_jti_blacklisted('secret_token_blacklisted'))

    def test_business_model(self):
        """Test whether business model is working."""

        self.user.save()
        query_user = User.query.filter_by(email='test@andela.com').first()

        business = Business('CosmasTech', 'Technology', 'Nairobi',
                            'AI is transforming human life', query_user.id)
        business.save()

        query_res = Business.query.filter_by(id=1).first()
        self.assertEqual(query_res.name, 'CosmasTech')

    def test_reviews_model(self):
        """Test whether review model is working."""

        self.user.save()
        query_user = User.query.filter_by(email='test@andela.com').first()

        business = Business('CosmasTech', 'Technology', 'Nairobi',
                            'AI is transforming human life', query_user.id)
        business.save()
        query_business = Business.query.filter_by(name='CosmasTech').first()

        review = Reviews('The business will really save the world!',
                         query_business.id, query_user.id)
        review.save()
        query_reviews = Reviews.query.filter_by(id=1).first()

        self.assertEqual(
            query_reviews.review, 'The business will really save the world!')


if __name__ == '__main__':
    unittest.main()
