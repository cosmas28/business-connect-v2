"""Design test case to test business related endpoints.

This module design test suite into which contains test cases for behaviors that
are expected from API endpoints.

"""


import unittest
from flask import json

from run import app
from app.models.business import Business


class TestBusinessEndpointsTestCase(unittest.TestCase):
    """Illustrate test cases to test expected behavior of business API endpoints. """

    def setUp(self):
        """Enter business records int business records dictionary so that it can be reused by other test cases."""
        self.run_app = app.test_client()
        self.business = Business()
        self.headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        self.business_record = {
            'business_id': 1,
            'business_owner': 'Cosmas',
            'business_name': 'Cosma Tech',
            'business_category': 'Technology',
            'business_location': 'Arusha',
            'business_summary': 'Internet of things is making the world a better place'
        }
        self.user_data = {
            'username': 'cosmas',
            'password': 'andela2018',
            'confirm_password': 'andela2018'
        }
        json_data = json.dumps(self.user_data)
        self.response = self.run_app.post('/api/v1/register_user', data=json_data, headers=self.headers)
        self.business.create_business(1, 'cosmas', 'Cosma Tech', 'Nairobi', 'Technology', 'Masters of ecommerce')
        self.business.create_business(2, 'Allan', 'Allan Tech', 'Kitale', 'Technology', 'Cryptocurrency')

    def tearDown(self):
        """Delete registered business records after every test case has run."""

        for key in list(self.business.business_records.keys()):
            del self.business.business_records[key]

    def test_register_business_endpoint(self):
        """Test business API endpoint can register new business with POST request."""

        json_data = json.dumps(self.business_record)
        response = self.run_app.post('/api/v1/business', data=json_data, headers=self.headers)
        self.assertEqual(response.status_code, 201)

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


if __name__ == '__main__':
    unittest.main()
