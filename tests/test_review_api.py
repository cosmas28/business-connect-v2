"""Design test case to test reviews API endpoints."""

import unittest

from flask import json
from . import app
from app.models import db


class ReviewsTestCase(unittest.TestCase):
    """Test suite for reviews functionality."""

    def setUp(self):
        """Call this before every test."""

        db.app = app
        db.create_all()

        self.run_app = app.test_client()
        self.headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}

    def register_user(self):
        user_data = json.dumps({'email': 'test@andela.com', 'username': 'cosmas', 'first_name': 'first',
                                'last_name': 'last', 'password': 'andela2018', 'confirm_password': 'andela2018'})
        return self.run_app.post('/api/v1/auth/register_user', data=user_data, headers=self.headers)

    def login_user(self):
        login_data = json.dumps({'email': 'test@andela.com', 'password': 'andela2018'})

        return self.run_app.post('/api/v1/auth/login_user', data=login_data, headers=self.headers)

    def tearDown(self):
        """Call after every test to remove the created table."""

        db.session.remove()
        db.drop_all()

    def test_empty_review(self):
        """Test whether user have provided a business review."""

        self.register_user()
        login_response = self.login_user()
        access_token = json.loads(login_response.data.decode())['access_token']

        business_data = json.dumps({'name': 'Palmer Tech', 'category': 'Technology', 'location': 'Nairobi',
                                    'summary': 'AI is transforming human life'})
        self.run_app.post('/api/v1/businesses', data=business_data,
                          headers=dict(Authorization="Bearer " + access_token))

        review = json.dumps({'review': ''})
        review_res = self.run_app.post('/api/v1/businesses/1/reviews', data=review,
                                       headers=dict(Authorization="Bearer " + access_token))

        self.assertEqual(json.loads(review_res.data.decode())['response_message'], 'Review value is empty!')

    def test_user_can_add_review(self):
        """Test whether user add a business review."""

        self.register_user()
        login_response = self.login_user()
        access_token = json.loads(login_response.data.decode())['access_token']

        business_data = json.dumps({'name': 'Palmer Tech', 'category': 'Technology', 'location': 'Nairobi',
                                    'summary': 'AI is transforming human life'})
        self.run_app.post('/api/v1/businesses', data=business_data,
                          headers=dict(Authorization="Bearer " + access_token))

        review = json.dumps({'review': 'The future of AI is very bright, mostly in security'})
        review_res = self.run_app.post('/api/v1/businesses/1/reviews', data=review,
                                       headers=dict(Authorization="Bearer " + access_token))

        self.assertEqual(json.loads(review_res.data.decode())['response_message'],
                         'Review has been added successfully!')


if __name__ == '__main__':
    unittest.main()
