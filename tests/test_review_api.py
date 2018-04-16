"""Design test case to test reviews API endpoints."""

import unittest

from flask import json
from app.models import db
from . import app


class BusinessReviewsTest(unittest.TestCase):
    """Test suite for business reviews functionality."""

    def setUp(self):
        """Call this before every test."""

        db.app = app
        db.create_all()

        self.run_app = app.test_client()
        self.headers = {'Content-type': 'application/json',
                        'Accept': 'text/plain'}

    def register_user(self):
        """Register a user."""

        user_data = json.dumps({
            'email': 'test@andela.com', 'username': 'cosmas',
            'first_name': 'first', 'last_name': 'last',
            'password': 'andela2018', 'confirm_password': 'andela2018'})
        return self.run_app.post('/api/v2/auth/register',
                                 data=user_data, headers=self.headers)

    def login_user(self):
        """Register a user."""
        login_data = json.dumps({'email': 'test@andela.com',
                                 'password': 'andela2018'})

        return self.run_app.post('/api/v2/auth/login',
                                 data=login_data, headers=self.headers)

    def register_business(self, access_token):
        """Register a business."""

        business_data = json.dumps({
            'name': 'Palmer Tech', 'category': 'Technology',
            'location': 'Nairobi', 'summary': 'AI is transforming human life'})
        return self.run_app.post(
            '/api/v2/businesses', data=business_data,
            headers=dict(Authorization='Bearer ' + access_token))

    def add_review(self, access_token):
        """Register a business review"""

        review = json.dumps({
            'review': 'The future of AI is very bright, mostly in security'})
        return self.run_app.post(
            '/api/v2/businesses/1/reviews', data=review,
            headers=dict(Authorization='Bearer ' + access_token))

    def tearDown(self):
        """Call after every test to remove the created table."""

        db.session.remove()
        db.drop_all()

    def test_add_null_business_id(self):
        """Test business review with null business id
        using post request for BusinessReviews class view."""

        self.register_user()
        login_response = self.login_user()
        access_token = json.loads(login_response.data.decode())['access_token']

        self.register_business(access_token)

        review = json.dumps({
            'review': 'The future of AI is very bright, mostly in security'})
        review_res = self.run_app.post(
            '/api/v2/businesses/reviews', data=review,
            headers=dict(Authorization='Bearer ' + access_token))

        self.assertEqual(review_res.status_code, 404)

    def test_add_null_review(self):
        """Test business review with null review
        using post request for BusinessReviews class view."""

        self.register_user()
        login_response = self.login_user()
        access_token = json.loads(login_response.data.decode())['access_token']

        self.register_business(access_token)

        review = json.dumps({'review': ''})
        review_res = self.run_app.post(
            '/api/v2/businesses/1/reviews', data=review,
            headers=dict(Authorization='Bearer ' + access_token))

        self.assertEqual(review_res.status_code, 406)

    def test_add_successful(self):
        """Test business reviewed successfully
        using post request for BusinessReviews class view."""

        self.register_user()
        login_response = self.login_user()
        access_token = json.loads(login_response.data.decode())['access_token']

        self.register_business(access_token)
        review_res = self.add_review(access_token)

        self.assertEqual(
            json.loads(review_res.data.decode())['response_message'],
            'Review has been added successfully!')

    def test_view_unregistered_business(self):
        """Test view unregistered business reviews
        using get request for BusinessReviews class view."""

        self.register_user()
        login_response = self.login_user()
        access_token = json.loads(login_response.data.decode())['access_token']

        self.register_business(access_token)

        review = json.dumps({
            'review': 'The future of AI is very bright, mostly in security'})
        review_res = self.run_app.get(
            '/api/v2/businesses/reviews', data=review,
            headers=dict(Authorization='Bearer ' + access_token))

        self.assertEqual(review_res.status_code, 404)

    def test_view_successful(self):
        """Test view a business reviews successfully
        using get request for BusinessReviews class view."""

        self.register_user()
        login_response = self.login_user()
        access_token = json.loads(login_response.data.decode())['access_token']

        self.register_business(access_token)
        self.add_review(access_token)

        response = self.run_app.get(
            '/api/v2/businesses/1/reviews',
            headers=dict(Authorization='Bearer ' + access_token))

        self.assertIn(
            'The future of AI is very bright, mostly in security',
            str(response.data))


if __name__ == '__main__':
    unittest.main()
