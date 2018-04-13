"""Design test case to test user account related functionalities.

This module design test suite in which contains test cases for behaviors that
are expected from user account authentication.

"""

import unittest

from flask import json

from app.models import User
from app.models import db
from . import app


class AbstractTest(unittest.TestCase):
    """Define methods to be used in all test suites."""

    def setUp(self):
        """Call this before every test."""

        db.app = app
        db.create_all()

        self.run_app = app.test_client()
        self.headers = {'Content-type': 'application/json',
                        'Accept': 'text/plain'}

        self.user_data = json.dumps({'email': 'test2@andela.com',
                                     'username': 'testuser',
                                     'first_name': 'first',
                                     'last_name': 'last',
                                     'password': 'andela2018',
                                     'confirm_password': 'andela2018'})

    def tearDown(self):
        """Call after every test to remove the created table."""

        db.session.remove()
        db.drop_all()


class RegisterUserTest(AbstractTest):
    """Illustrate test cases for user registration view."""

    def test_empty_email(self):
        """Test whether user have provided an email."""

        user_data = json.dumps({'email': '', 'username': 'cosmas',
                                'first_name': 'first',
                                'last_name': 'last', 'password': 'andela2018',
                                'confirm_password': 'andela2018'})
        response = self.run_app.post('/api/v2/auth/register',
                                     data=user_data, headers=self.headers)

        json_res = json.loads(response.data.decode())
        self.assertEqual(json_res['message'],
                         'Email and Username are required!')

    def test_empty_username(self):
        """Test whether user have not provided a username."""

        user_data = json.dumps({'email': 'test@andela.com',
                                'username': '', 'password': 'andela2018',
                                'confirm_password': 'andela2018'})
        response = self.run_app.post('/api/v2/auth/register',
                                     data=user_data, headers=self.headers)
        json_res = json.loads(response.data.decode())
        self.assertEqual(json_res['message'],
                         'Email and Username are required!')

    def test_empty_password(self):
        """Test whether user have provided password."""

        user_data = json.dumps({'email': 'test@andela.com',
                                'username': 'cosmas', 'password': '',
                                'confirm_password': 'andela2018'})
        response = self.run_app.post('/api/v2/auth/register',
                                     data=user_data, headers=self.headers)
        json_res = json.loads(response.data.decode())
        self.assertEqual(json_res['message'],
                         'Password and Confirmation password are required!')

    def test_empty_password_confirm(self):
        """Test whether user have provided confirmation password."""

        user_data = json.dumps({'email': 'test@andela.com',
                                'username': 'cosmas', 'password': 'andela2018',
                                'confirm_password': ''})
        response = self.run_app.post('/api/v2/auth/register',
                                     data=user_data, headers=self.headers)
        json_res = json.loads(response.data.decode())
        self.assertEqual(json_res['message'],
                         'Password and Confirmation password are required!')

    def test_duplicate_email(self):
        """Test whether the email address exist."""

        user = User('test@andela.com', 'testuser',
                    'first', 'last', 'password')
        user.save()

        user_data = json.dumps({'email': 'test@andela.com',
                                'username': 'cosmas', 'first_name': 'first',
                                'last_name': 'last', 'password': 'andela2018',
                                'confirm_password': 'andela2018'})
        response = self.run_app.post('/api/v2/auth/register',
                                     data=user_data, headers=self.headers)

        json_res = json.loads(response.data.decode())
        self.assertEqual(json_res['message'], 'User already exists. Sign in!')

    def test_duplicate_username(self):
        """Test whether the username exist."""

        user = User('test@andela.com', 'testuser', 'first', 'last', 'password')
        user.save()

        user_data = json.dumps({'email': 'test2@andela.com',
                                'username': 'testuser', 'first_name': 'first',
                                'last_name': 'last', 'password': 'andela2018',
                                'confirm_password': 'andela2018'})
        response = self.run_app.post('/api/v2/auth/register',
                                     data=user_data, headers=self.headers)

        json_res = json.loads(response.data.decode())
        self.assertEqual(json_res['message'], 'User already exists. Sign in!')

    def test_password_length(self):
        """Test user password to be more than 6 characters."""

        user_data = json.dumps({'email': 'test2@andela.com',
                                'username': 'testuser', 'first_name': 'first',
                                'last_name': 'last', 'password': 'a2018',
                                'confirm_password': 'a2018'})
        response = self.run_app.post('/api/v2/auth/register',
                                     data=user_data, headers=self.headers)
        json_res = json.loads(response.data.decode())
        self.assertEqual(json_res['message'],
                         'Password must be more than 6 characters!')

    def test_password_confirmation(self):
        """Test user password match confirmation password."""

        user_data = json.dumps({'email': 'test2@andela.com',
                                'username': 'testuser', 'first_name': 'first',
                                'last_name': 'last', 'password': 'andela2014',
                                'confirm_password': 'andela2018'})
        response = self.run_app.post('/api/v2/auth/register',
                                     data=user_data, headers=self.headers)
        json_res = json.loads(response.data.decode())
        self.assertEqual(json_res['message'],
                         'Password does not match the confirmation password!')

    def test_user_can_create_account(self):
        """
            Test registerUser API endpoint can
             register a new user with POST request.
        """

        user_data = json.dumps({'email': 'test2@andela.com',
                                'username': 'testuser', 'first_name': 'first',
                                'last_name': 'last', 'password': 'andela2018',
                                'confirm_password': 'andela2018'})
        response = self.run_app.post('/api/v2/auth/register',
                                     data=user_data, headers=self.headers)
        json_res = json.loads(response.data.decode())
        self.assertEqual(json_res['message'],
                         'You have successfully created an account!')
        registered_user = User.query.filter_by(
            email='test2@andela.com').first()
        self.assertTrue(registered_user)


class LoginUserTest(AbstractTest):
    """Test case for the login api endpoint."""

    def test_user_login_email(self):
        """Test whether user have provided existed email."""

        self.run_app.post('/api/v2/auth/register',
                          data=self.user_data, headers=self.headers)

        login_data = json.dumps({'email': 'test@andela.com',
                                 'password': 'andela2018'})
        login_response = self.run_app.post('/api/v2/auth/login',
                                           data=login_data,
                                           headers=self.headers)

        # get the response text in json format
        json_res = json.loads(login_response.data.decode())
        self.assertEqual(json_res['response_message'], 'Invalid email!')
        # self.assertEqual(login_response.status_code, 401)
        self.assertEqual(json_res['status_code'], 401)

    def test_user_login_wrong_password(self):
        """Test whether user have provided a correct password."""

        self.run_app.post('/api/v2/auth/register',
                          data=self.user_data, headers=self.headers)

        login_data = json.dumps({'email': 'test2@andela.com',
                                 'password': 'andela2017'})
        login_response = self.run_app.post('/api/v2/auth/login',
                                           data=login_data,
                                           headers=self.headers)

        # get the response text in json format
        json_res = json.loads(login_response.data.decode())
        self.assertEqual(json_res['response_message'],
                         'Invalid email or password!')
        # self.assertEqual(login_response.status_code, 401)
        self.assertEqual(json_res['status_code'], 401)

    def test_user_can_login(self):
        """Test registered user can login."""

        self.run_app.post('/api/v2/auth/register',
                          data=self.user_data, headers=self.headers)

        login_data = json.dumps({'email': 'test2@andela.com',
                                 'password': 'andela2018'})
        login_response = self.run_app.post('/api/v2/auth/login',
                                           data=login_data,
                                           headers=self.headers)

        json_res = json.loads(login_response.data.decode())
        self.assertEqual(json_res['response_message'],
                         'You logged in successfully!')
        self.assertEqual(json_res['status_code'], 200)
        self.assertTrue(json_res['access_token'])

    def test_access_token_logout(self):
        """Test whether user can logout by revoking access token."""

        register_res = self.run_app.post('/api/v2/auth/register',
                                         data=self.user_data,
                                         headers=self.headers)
        json_res = json.loads(register_res.data.decode())
        self.assertEqual(json_res['message'],
                         'You have successfully created an account!')

        login_data = json.dumps({'email': 'test2@andela.com',
                                 'password': 'andela2018'})
        login_response = self.run_app.post('/api/v2/auth/login',
                                           data=login_data,
                                           headers=self.headers)
        access_token = json.loads(login_response.data.decode())['access_token']

        logout_res = self.run_app.post(
            '/api/v2/auth/logout',
            headers=dict(Authorization='Bearer ' + access_token))
        self.assertEqual(
            json.loads(logout_res.data.decode())['status_code'], 200)
        self.assertEqual(
            json.loads(logout_res.data.decode())['response_message'],
            'Log out has been successful!')

    def test_refresh_token_logout(self):
        """Test whether user can logout by revoking jwt refresh token."""

        self.run_app.post('/api/v2/auth/register',
                          data=self.user_data, headers=self.headers)

        login_data = json.dumps({'email': 'test2@andela.com',
                                 'password': 'andela2018'})
        login_response = self.run_app.post('/api/v2/auth/login',
                                           data=login_data,
                                           headers=self.headers)
        refresh_token = json.loads(
            login_response.data.decode())['refresh_token']

        logout_res = self.run_app.post(
            '/api/v2/auth/logout_refresh_token',
            headers=dict(Authorization='Bearer ' + refresh_token))
        self.assertEqual(
            json.loads(logout_res.data.decode())['status_code'], 200)
        self.assertEqual(
            json.loads(logout_res.data.decode())['response_message'],
            'Log out has been successful!')


class ResetPasswordTest(AbstractTest):
    """Test case for the reset password api endpoint."""

    def test_empty_email(self):
        """Test whether user have provided an email."""

        self.run_app.post('/api/v2/auth/register',
                          data=self.user_data, headers=self.headers)

        new_data = json.dumps({'email': '', 'password': 'andela2018',
                               'confirm_password': 'andela2018'})
        response = self.run_app.post('/api/v2/auth/reset_password',
                                     data=new_data, headers=self.headers)

        # get the response text in json format
        json_res = json.loads(response.data.decode())
        self.assertEqual(json_res['response_message'], 'Email is required!')

    def test_empty_password(self):
        """Test whether user have provided a password."""

        self.run_app.post('/api/v2/auth/register',
                          data=self.user_data, headers=self.headers)

        new_data = json.dumps({'email': 'test@andela.com', 'password': '',
                               'confirm_password': 'andela2018'})
        response = self.run_app.post('/api/v2/auth/reset_password',
                                     data=new_data, headers=self.headers)

        # get the response text in json format
        json_res = json.loads(response.data.decode())
        self.assertEqual(json_res['response_message'], 'Password is required!')

    def test_empty_password_confirm(self):
        """Test whether user have provided confirmation password."""

        self.run_app.post('/api/v2/auth/register',
                          data=self.user_data, headers=self.headers)

        new_data = json.dumps({'email': 'test@andela.com',
                               'password': 'andela2018',
                               'confirm_password': ''})
        response = self.run_app.post('/api/v2/auth/reset_password',
                                     data=new_data, headers=self.headers)

        # get the response text in json format
        json_res = json.loads(response.data.decode())
        self.assertEqual(json_res['response_message'], 'Password is required!')

    def test_registered_email(self):
        """Test whether user have provided registered email."""

        self.run_app.post('/api/v2/auth/register',
                          data=self.user_data, headers=self.headers)

        new_data = json.dumps({'email': 'not_registered@andela.com',
                               'password': 'andela2018',
                               'confirm_password': 'andela2018'})
        response = self.run_app.post('/api/v2/auth/reset_password',
                                     data=new_data, headers=self.headers)

        # get the response text in json format
        json_res = json.loads(response.data.decode())
        self.assertEqual(json_res['response_message'], 'Email not registered')

    def test_user_reset_password(self):
        """Test registered user can reset their passwords."""

        self.run_app.post('/api/v2/auth/register',
                          data=self.user_data, headers=self.headers)

        new_data = json.dumps({'email': 'test2@andela.com',
                               'password': 'andela2018',
                               'confirm_password': 'andela2018'})
        response = self.run_app.post('/api/v2/auth/reset_password',
                                     data=new_data, headers=self.headers)

        # get the response text in json format
        json_res = json.loads(response.data.decode())
        self.assertEqual(json_res['response_message'],
                         'Password reset successfully!')
        self.assertEqual(json_res['status_code'], 200)


if __name__ == '__main__':
    unittest.main()
