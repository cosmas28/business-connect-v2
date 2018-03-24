"""Design test case to test user account related functionalities.

This module design test suite in which contains test cases for behaviors that
are expected from user account authentication.

"""

import unittest

from flask import json

from . import app
from app.models.user import db, User


class AbstractTest(unittest.TestCase):

    def setUp(self):
        """Call this before every test."""

        db.app = app
        db.create_all()

        self.run_app = app.test_client()
        self.headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}

    def tearDown(self):
        """Call after every test to remove the created table."""

        db.session.remove()
        db.drop_all()

    def test_empty_email(self):
        """Test whether user have provided an email."""

        user_data = json.dumps({'username': 'cosmas', 'first_name': 'first',
                                'last_name': 'last', 'password': 'andela2018', 'confirm_password': 'andela2018'})
        response = self.run_app.post('/api/v1/register_user', data=user_data, headers=self.headers)
        self.assertEqual(response.status_code, "Email is required!")

    def test_empty_username(self):
        """Test whether user have not provided a username."""

        user_data = json.dumps({'email': 'test@andela.com', 'first_name': 'first',
                                'last_name': 'last', 'password': 'andela2018', 'confirm_password': 'andela2018'})
        response = self.run_app.post('/api/v1/register_user', data=user_data, headers=self.headers)
        self.assertEqual(response.status_code, "Username is required!")

    def test_empty_firstname(self):
        """Test whether user have provided first name."""

        user_data = json.dumps({'email': 'test@andela.com', 'username': 'cosmas',
                                'last_name': 'last', 'password': 'andela2018', 'confirm_password': 'andela2018'})
        response = self.run_app.post('/api/v1/register_user', data=user_data, headers=self.headers)
        self.assertEqual(response.status_code, "First name is required!")

    def test_empty_lastname(self):
        """Test whether user have provided last name."""

        user_data = json.dumps({'email': 'test@andela.com', 'username': 'cosmas', 'first_name': 'first',
                                'password': 'andela2018', 'confirm_password': 'andela2018'})
        response = self.run_app.post('/api/v1/register_user', data=user_data, headers=self.headers)
        self.assertEqual(response.status_code, "Last name is required!")

    def test_empty_password(self):
        """Test whether user have provided password."""

        user_data = json.dumps({'email': 'test@andela.com', 'username': 'cosmas', 'first_name': 'first',
                                'last_name': 'last', 'confirm_password': 'andela2018'})
        response = self.run_app.post('/api/v1/register_user', data=user_data, headers=self.headers)
        self.assertEqual(response.status_code, "Password is required!")

    def test_empty_password_confirm(self):
        """Test whether user have provided confirmation password."""

        user_data = json.dumps({'email': 'test@andela.com', 'username': 'cosmas', 'first_name': 'first',
                                'last_name': 'last', 'password': 'andela2018',})
        response = self.run_app.post('/api/v1/register_user', data=user_data, headers=self.headers)
        self.assertEqual(response.status_code, "Confirmation password is required!")

    def test_duplicate_email(self):
        """Test whether the email address exist."""

        user = User('test@andela.com', 'testuser', 'first', 'last', 'password')
        db.session.add(user)
        db.session.commit()

        user_data = json.dumps({'email': 'test@andela.com', 'username': 'cosmas', 'first_name': 'first',
                                'last_name': 'last', 'password': 'andela2018', 'confirm_password': 'andela2018'})
        response = self.run_app.post('/api/v1/register_user', data=user_data, headers=self.headers)
        self.assertEqual(response, 'The email address already exist!')

    def test_duplicate_username(self):
        """Test whether the username exist."""

        user = User('test@andela.com', 'testuser', 'first', 'last', 'password')
        db.session.add(user)
        db.session.commit()

        user_data = json.dumps({'email': 'test@andela.com', 'username': 'testuser', 'first_name': 'first',
                                'last_name': 'last', 'password': 'andela2018', 'confirm_password': 'andela2018'})
        response = self.run_app.post('/api/v1/register_user', data=user_data, headers=self.headers)
        self.assertEqual(response, 'The username already exist!')

    def test_password_length(self):
        """Test user password to be more than 6 characters."""

        user_data = json.dumps({'email': 'test@andela.com', 'username': 'cosmas', 'first_name': 'first',
                                'last_name': 'last', 'password': 'a2018', 'confirm_password': 'a2018'})
        response = self.run_app.post('/api/v1/register_user', data=user_data, headers=self.headers)
        self.assertEqual(response, 'Password must be more than 6 characters!')

    def test_password_confirmation(self):
        """Test user password match confirmation password."""

        user_data = json.dumps({'email': 'test@andela.com', 'username': 'cosmas', 'first_name': 'first',
                                'last_name': 'last', 'password': 'andela2018', 'confirm_password': 'andela2017'})
        response = self.run_app.post('/api/v1/register_user', data=user_data, headers=self.headers)
        self.assertEqual(response, 'The password does not match!')

    def test_user_can_create_account(self):
        """Test registerUser API endpoint can register a new user with POST request."""

        user_data = json.dumps({'email': 'test@andela.com', 'username': 'cosmas', 'first_name': 'first',
                                'last_name': 'last', 'password': 'andela2018', 'confirm_password': 'andela2018'})
        response = self.run_app.post('/api/v1/register_user', data=user_data, headers=self.headers)
        self.assertEqual(response.status_code, "You have successfully created an account!")


if __name__ == '__main__':
    unittest.main()