"""Design test case to test business related endpoints.

This module design test suite into which contains test cases for behaviors that
are expected from API endpoints.

"""


import unittest
from flask import json

from run import app
from tests import business


class TestBusinessEndpointsTestCase(unittest.TestCase):
    """Illustrate test cases to test expected behavior of business API endpoints. """

    def setUp(self):
        """Enter business records int business records dictionary so that it can be reused by other test cases."""

        self.run_app = app.test_client()
        self.headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        self.business_record = {
            'business_id': 1,
            'business_owner': 'Cosmas',
            'business_name': 'Cosma Tech',
            'business_category': 'Technology',
            'business_location': 'Arusha',
            'business_summary': 'Internet of things is making the world a better place'
        }
        json_data = json.dumps(self.business_record)
        self.business_res = self.run_app.post('/api/v1/business', data=json_data, headers=self.headers)
        self.user_data = {
            'username': 'cosmas',
            'password': 'andela2018',
            'confirm_password': 'andela2018'
        }
        json_data = json.dumps(self.user_data)
        self.response = self.run_app.post('/api/v1/register_user', data=json_data, headers=self.headers)

    def tearDown(self):
        """Delete registered business records after every test case has run."""

        self.run_app.delete('/api/v1/businesses/1')

    def test_register_business_endpoint(self):
        """Test business API endpoint can register new business with POST request."""

        self.assertEqual(self.business_res.status_code, 201)

    def test_view_businesses_endpoint(self):
        """Test whether a get request to business API endpoint has succeeded."""

        response = self.run_app.get('/api/v1/business')
        self.assertEqual(response.status_code, 200)

    def test_view_businesses_by_id_endpoint(self):
        """Test whether providing business id to a get request to business API endpoint has succeeded."""
       
        response = self.run_app.get('/api/v1/businesses/1')
        self.assertEqual(response.status_code, 200)

    def test_user_can_register(self):
        """Test registerUser API endpoint can register a new user with POST request."""

        self.assertEqual(self.response.status_code, 201)

    def test_user_can_login(self):
        """Test login user API endpoint can login a user with POST request."""

        login_data = json.dumps({'username': 'cosmas', 'password': 'andela2018'})
        response = self.run_app.post('/api/v1/login_user', data=login_data, headers=self.headers)
        self.assertEqual(response.status_code, 200)

    def test_user_can_logout(self):
        """Test log out user API endpoint can log out a user with POST request."""

        login_data = json.dumps({'username': 'cosmas', 'password': 'andela2018'})
        self.run_app.post('/api/v1/login_user', data=login_data, headers=self.headers)
        response = self.run_app.post('/api/v1/logout', data=json.dumps({'username': 'cosmas'}), headers=self.headers)
        self.assertEqual(response.status_code, 200)

    def test_user_can_reset_password(self):
        """Test reset password API endpoint reset user password with POST request."""

        new_password = json.dumps({'username': 'cosmas', 'password': 'andela2022'})
        response = self.run_app.post('/api/v1/reset-password', data=new_password, headers=self.headers)
        self.assertEqual(response.status_code, 201)

    def test_user_can_delete_business(self):
        """Test whether a user can delete a business with DELETE request."""

        response = self.run_app.delete('/api/v1/businesses/1')
        self.assertEqual(response.status_code, 200)

    def test_user_can_update_business(self):
        """Test whether a user can update a business using PUT request."""

        new_info = json.dumps({
            'business_owner': 'Cosmas',
            'business_name': 'Cosma Tech',
            'business_category': 'Technology',
            'business_location': 'Arusha',
            'business_summary': 'IoT is making our world smart'
        })
        response = self.run_app.put('/api/v1/businesses/1', data=new_info, headers=self.headers)
        self.assertEqual(response.status_code, 200)


class TestReviewsEndpoints(unittest.TestCase):
    def setUp(self):
        self.run_app = app.test_client()
        self.headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        business.create_business(1, 'Cosmas', 'Cosma Tech', 'Nairobi', 'Technology',
                                              'Masters of ecommerce')

    def test_user_can_add_reviews(self):
        """Test whether a user can add a business review using POST request."""

        json_data = json.dumps({
            'review': 'first review'
        })
        response = self.run_app.post('/api/v1/businesses/1/reviews', data=json_data, headers=self.headers)
        self.assertEqual(response.status_code, 201)


if __name__ == '__main__':
    unittest.main()
