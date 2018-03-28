"""Design test case to test business review related functionalities.

This module design test suite in which contains test cases for behaviors that
are expected from review model.

"""


import unittest

from . import app
from app.models.user import Reviews, User, Business
from app.models import db


class AddReviewTest(unittest.TestCase):

    """Illustrate test cases to test expected behavior of add reviews functionality. """

    def setUp(self):
        """Call this before every test."""

        db.app = app
        db.create_all()

    def tearDown(self):
        """Call after every test to remove the created table."""

        db.session.remove()
        db.drop_all()

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
