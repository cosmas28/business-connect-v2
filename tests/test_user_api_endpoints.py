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

        self.user_data = json.dumps({'email': 'test@andela.com', 'username': 'cosmas', 'first_name': 'first',
                                     'last_name': 'last', 'password': 'andela2018', 'confirm_password': 'andela2018'})

    def tearDown(self):
        """Call after every test to remove the created table."""

        db.session.remove()
        db.drop_all()


class RegisterUserTest(AbstractTest):

    def test_empty_email(self):
        """Test whether user have provided an email."""

        user_data = json.dumps({'email': '', 'username': 'cosmas', 'first_name': 'first',
                                'last_name': 'last', 'password': 'andela2018', 'confirm_password': 'andela2018'})
        response = self.run_app.post('/api/v1/auth/register_user', data=user_data, headers=self.headers)
        self.assertEqual(response.status_code, 406)

    def test_empty_username(self):
        """Test whether user have not provided a username."""

        user_data = json.dumps({'email': 'test@andela.com', 'username': '', 'first_name': 'first',
                                'last_name': 'last', 'password': 'andela2018', 'confirm_password': 'andela2018'})
        response = self.run_app.post('/api/v1/auth/register_user', data=user_data, headers=self.headers)
        self.assertEqual(response.status_code, 406)

    def test_empty_firstname(self):
        """Test whether user have provided first name."""

        user_data = json.dumps({'email': 'test@andela.com', 'username': 'cosmas', 'first_name': '',
                                'last_name': 'last', 'password': 'andela2018', 'confirm_password': 'andela2018'})
        response = self.run_app.post('/api/v1/auth/register_user', data=user_data, headers=self.headers)
        self.assertEqual(response.status_code, 406)

    def test_empty_lastname(self):
        """Test whether user have provided last name."""

        user_data = json.dumps({'email': 'test@andela.com', 'username': 'cosmas', 'first_name': 'first',
                                'last_name': '', 'password': 'andela2018', 'confirm_password': 'andela2018'})
        response = self.run_app.post('/api/v1/auth/register_user', data=user_data, headers=self.headers)
        self.assertEqual(response.status_code, 406)

    def test_empty_password(self):
        """Test whether user have provided password."""

        user_data = json.dumps({'email': 'test@andela.com', 'username': 'cosmas', 'first_name': 'first',
                                'last_name': 'last', 'password': '', 'confirm_password': 'andela2018'})
        response = self.run_app.post('/api/v1/auth/register_user', data=user_data, headers=self.headers)
        self.assertEqual(response.status_code, 406)

    def test_empty_password_confirm(self):
        """Test whether user have provided confirmation password."""

        user_data = json.dumps({'email': 'test@andela.com', 'username': 'cosmas', 'first_name': 'first',
                                'last_name': 'last', 'password': 'andela2018', 'confirm_password': ''})
        response = self.run_app.post('/api/v1/auth/register_user', data=user_data, headers=self.headers)
        self.assertEqual(response.status_code, 406)

    def test_duplicate_email(self):
        """Test whether the email address exist."""

        user = User('test@andela.com', 'testuser', 'first', 'last', 'password')
        db.session.add(user)
        db.session.commit()

        user_data = json.dumps({'email': 'test@andela.com', 'username': 'cosmas', 'first_name': 'first',
                                'last_name': 'last', 'password': 'andela2018', 'confirm_password': 'andela2018'})
        response = self.run_app.post('/api/v1/auth/register_user', data=user_data, headers=self.headers)
        self.assertEqual(response.status_code, 406)

    def test_duplicate_username(self):
        """Test whether the username exist."""

        user = User('test@andela.com', 'testuser', 'first', 'last', 'password')
        db.session.add(user)
        db.session.commit()

        user_data = json.dumps({'email': 'test2@andela.com', 'username': 'testuser', 'first_name': 'first',
                                'last_name': 'last', 'password': 'andela2018', 'confirm_password': 'andela2018'})
        response = self.run_app.post('/api/v1/auth/register_user', data=user_data, headers=self.headers)
        self.assertEqual(response.status_code, 406)

    def test_password_length(self):
        """Test user password to be more than 6 characters."""

        user_data = json.dumps({'email': 'test@andela.com', 'username': 'cosmas', 'first_name': 'first',
                                'last_name': 'last', 'password': 'a2018', 'confirm_password': 'a2018'})
        response = self.run_app.post('/api/v1/auth/register_user', data=user_data, headers=self.headers)
        self.assertEqual(response.status_code, 406)

    def test_password_confirmation(self):
        """Test user password match confirmation password."""

        user_data = json.dumps({'email': 'test@andela.com', 'username': 'cosmas', 'first_name': 'first',
                                'last_name': 'last', 'password': 'andela2018', 'confirm_password': 'andela2017'})
        response = self.run_app.post('/api/v1/auth/register_user', data=user_data, headers=self.headers)
        self.assertEqual(response.status_code, 406)

    def test_user_can_create_account(self):
        """Test registerUser API endpoint can register a new user with POST request."""

        user_data = json.dumps({'email': 'test@andela.com', 'username': 'cosmas', 'first_name': 'first',
                                'last_name': 'last', 'password': 'andela2018', 'confirm_password': 'andela2018'})
        response = self.run_app.post('/api/v1/auth/register_user', data=user_data, headers=self.headers)
        self.assertEqual(response.status_code, 201)


class LoginUserTest(AbstractTest):
    """Test case for the login api endpoint."""

    def test_user_login_empty_email_password(self):
        """Test whether user have provided an email and a password."""

        register_response = self.run_app.post('/api/v1/auth/register_user', data=self.user_data, headers=self.headers)
        self.assertEqual(register_response.status_code, 201)

        login_data = json.dumps({'email': '', 'password': ''})
        login_response = self.run_app.post('/api/v1/auth/login_user', data=login_data, headers=self.headers)

        # get the response text in json format
        json_res = json.loads(login_response.data.decode())
        self.assertEqual(json_res['response_message'], "Email and password is required!")

    def test_user_login_empty_email(self):
        """Test whether user have provided an email."""

        register_response = self.run_app.post('/api/v1/auth/register_user', data=self.user_data, headers=self.headers)
        self.assertEqual(register_response.status_code, 201)

        login_data = json.dumps({'email': '', 'password': 'andela2018'})
        login_response = self.run_app.post('/api/v1/auth/login_user', data=login_data, headers=self.headers)

        # get the response text in json format
        json_res = json.loads(login_response.data.decode())
        self.assertEqual(json_res['response_message'], "Email is required!")

    def test_user_login_empty_password(self):
        """Test whether user have provided a password."""

        register_response = self.run_app.post('/api/v1/auth/register_user', data=self.user_data, headers=self.headers)
        self.assertEqual(register_response.status_code, 201)

        login_data = json.dumps({'email': 'test@andela.com', 'password': ''})
        login_response = self.run_app.post('/api/v1/auth/login_user', data=login_data, headers=self.headers)

        # get the response text in json format
        json_res = json.loads(login_response.data.decode())
        self.assertEqual(json_res['response_message'], "Password is required!")

    def test_user_no_existed_login_email(self):
        """Test whether user have provided existed email."""

        register_response = self.run_app.post('/api/v1/auth/register_user', data=self.user_data, headers=self.headers)
        self.assertEqual(register_response.status_code, 201)

        login_data = json.dumps({'email': 'not_registered@andela.com', 'password': 'andela2018'})
        login_response = self.run_app.post('/api/v1/auth/login_user', data=login_data, headers=self.headers)

        # get the response text in json format
        json_res = json.loads(login_response.data.decode())
        self.assertEqual(json_res['response_message'], "Invalid email or password!")
        # self.assertEqual(login_response.status_code, 401)
        self.assertEqual(json_res['status_code'], 401)

    def test_user_login_wrong_password(self):
        """Test whether user have provided a correct password."""

        register_response = self.run_app.post('/api/v1/auth/register_user', data=self.user_data, headers=self.headers)
        self.assertEqual(register_response.status_code, 201)

        login_data = json.dumps({'email': 'test@andela.com', 'password': 'andela2017'})
        login_response = self.run_app.post('/api/v1/auth/login_user', data=login_data, headers=self.headers)

        # get the response text in json format
        json_res = json.loads(login_response.data.decode())
        self.assertEqual(json_res['response_message'], "Invalid email or password!")
        # self.assertEqual(login_response.status_code, 401)
        self.assertEqual(json_res['status_code'], 401)

    def test_user_can_login(self):
        """Test registered user can login."""

        register_response = self.run_app.post('/api/v1/auth/register_user', data=self.user_data, headers=self.headers)
        self.assertEqual(register_response.status_code, 201)

        login_data = json.dumps({'email': 'test@andela.com', 'password': 'andela2018'})
        login_response = self.run_app.post('/api/v1/auth/login_user', data=login_data, headers=self.headers)

        # get the response text in json format
        json_res = json.loads(login_response.data.decode())
        self.assertEqual(json_res['response_message'], "You logged in successfully!")
        # self.assertEqual(login_response.status_code, 200)
        self.assertEqual(json_res['status_code'], 200)
        self.assertTrue(json_res['access_token'])

    # def test_token_refresh_can_reissue_token(self):
    #     """Test reissue access token with refresh token."""
    #
    #     register_response = self.run_app.post('/api/v1/auth/register_user', data=self.user_data, headers=self.headers)
    #     self.assertEqual(register_response.status_code, 201)
    #
    #     login_data = json.dumps({'email': 'test@andela.com', 'password': 'andela2018'})
    #     login_response = self.run_app.post('/api/v1/auth/login_user', data=login_data, headers=self.headers)
    #
    #     # get the response text in json format
    #     json_res = json.loads(login_response.data.decode())
    #     self.assertEqual(json_res['status_code'], 200)
    #
    #     token_refresh = self.run_app.post('/api/v1/auth/refresh_token', headers=self.headers)
    #     json_token_ref = json.loads(token_refresh.data.decode())
    #     self.assertTrue(json_token_ref['access_token'])


if __name__ == '__main__':
    unittest.main()
