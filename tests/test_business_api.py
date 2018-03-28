"""Design test case to test user account related functionalities."""

import unittest

from flask import json
from . import app
from app.models.user import Business
from app.models import db


class AbstractTest(unittest.TestCase):

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

    def register_business(self):
        self.register_user()
        login_response = self.login_user()
        access_token = json.loads(login_response.data.decode())['access_token']

        business_data = json.dumps({'name': 'CosmasTech', 'category': 'Technology', 'location': 'Nairobi',
                                    'summary': 'AI is transforming human life'})

        return self.run_app.post('/api/v1/businesses', data=business_data,
                                 headers=dict(Authorization="Bearer " + access_token))

    def tearDown(self):
        """Call after every test to remove the created table."""

        db.session.remove()
        db.drop_all()


class CreateBusinessTest(AbstractTest):
    """Test suite for business registration functionality."""

    def test_empty_business_name(self):
        """Test whether user have not provided a business name."""

        self.register_user()
        login_response = self.login_user()
        access_token = json.loads(login_response.data.decode())['access_token']

        business_data = json.dumps({'name': '', 'category': 'Technology', 'location': 'Nairobi',
                                    'summary': 'AI is transforming human life'})

        response = self.run_app.post('/api/v1/businesses', data=business_data,
                                     headers=dict(Authorization="Bearer " + access_token))

        self.assertEqual(json.loads(response.data.decode())['response_message'], 'Business name is required!')

    def test_empty_business_category(self):
        """Test whether user have not provided a business category."""

        self.register_user()
        login_response = self.login_user()
        access_token = json.loads(login_response.data.decode())['access_token']

        business_data = json.dumps({'name': 'Cosmas Tech', 'category': '', 'location': 'Nairobi',
                                    'summary': 'AI is transforming human life'})

        response = self.run_app.post('/api/v1/businesses', data=business_data,
                                     headers=dict(Authorization="Bearer " + access_token))

        self.assertEqual(json.loads(response.data.decode())['response_message'], 'Business category is required!')

    def test_empty_business_location(self):
        """Test whether user have not provided a business location."""

        self.register_user()
        login_response = self.login_user()
        access_token = json.loads(login_response.data.decode())['access_token']

        business_data = json.dumps({'name': 'Cosmas Tech', 'category': 'Technology', 'location': '',
                                    'summary': 'AI is transforming human life'})

        response = self.run_app.post('/api/v1/businesses', data=business_data,
                                     headers=dict(Authorization="Bearer " + access_token))

        self.assertEqual(json.loads(response.data.decode())['response_message'], 'Business location is required!')

    def test_empty_business_summary(self):
        """Test whether user have not provided a business summary."""

        self.register_user()
        login_response = self.login_user()
        access_token = json.loads(login_response.data.decode())['access_token']

        business_data = json.dumps({'name': 'Cosmas Tech', 'category': 'Technology', 'location': 'Nairobi',
                                    'summary': ''})

        response = self.run_app.post('/api/v1/businesses', data=business_data,
                                     headers=dict(Authorization="Bearer " + access_token))

        self.assertEqual(json.loads(response.data.decode())['response_message'], 'Business summary is required!')

    def test_duplicate_business_name(self):
        """Test whether user have not provided a unique business name."""

        self.register_user()
        login_response = self.login_user()
        access_token = json.loads(login_response.data.decode())['access_token']
        first_business_data = json.dumps({'name': 'CosmasTech', 'category': 'Technology', 'location': 'Nairobi',
                                          'summary': 'AI is transforming human life'})

        self.run_app.post('/api/v1/businesses', data=first_business_data,
                          headers=dict(Authorization="Bearer " + access_token))

        business_data = json.dumps({'name': 'CosmasTech', 'category': 'Technology', 'location': 'Mombasa',
                                    'summary': 'IoT is transforming human security'})

        response = self.run_app.post('/api/v1/businesses', data=business_data,
                                     headers=dict(Authorization="Bearer " + access_token))

        self.assertEqual(json.loads(response.data.decode())['response_message'], 'Business name already registered!')

    def test_user_can_register_business(self):
        """Test whether user can successfully register a business."""

        self.register_user()
        login_response = self.login_user()
        access_token = json.loads(login_response.data.decode())['access_token']

        business_data = json.dumps({'name': 'Palmer Tech', 'category': 'Technology', 'location': 'Mombasa',
                                    'summary': 'IoT is transforming human security'})

        response = self.run_app.post('/api/v1/businesses', data=business_data,
                                     headers=dict(Authorization="Bearer " + access_token))

        self.assertEqual(json.loads(response.data.decode())['response_message'],
                         'Business has been registered successfully!')

    def test_user_can_view_all_businesses(self):
        """Test whether a user can view all registered businesses."""

        self.register_user()
        login_response = self.login_user()
        access_token = json.loads(login_response.data.decode())['access_token']

        business_data = json.dumps({'name': 'Palmer Tech', 'category': 'Technology', 'location': 'Mombasa',
                                    'summary': 'IoT is transforming human security'})
        self.run_app.post('/api/v1/businesses', data=business_data,
                          headers=dict(Authorization="Bearer " + access_token))

        response = self.run_app.get('/api/v1/businesses', headers=dict(Authorization="Bearer " + access_token))

        self.assertIn('Palmer Tech', str(response.data))


if __name__ == '__main__':
    unittest.main()
