"""Design test case to test user account related functionalities.

This module design test suite in which contains test cases for behaviors that
are expected from user account authentication.

"""

import unittest

from flask import json

from app.models import db
from app import create_app


class AbstractTest(unittest.TestCase):
    """Define methods to be used in all test suites."""

    def setUp(self):
        """Call this before every test."""

        self.app = create_app(config_object="testing")
        self.run_app = self.app.test_client()
        self.headers = {
            'Content-type': 'application/json', 'Accept': 'text/plain'}

        self.user_data = json.dumps({'email': 'test2@andela.com',
                                     'username': 'testuser',
                                     'first_name': 'first',
                                     'last_name': 'last',
                                     'password': 'andela2018',
                                     'confirm_password': 'andela2018'})

        with self.app.app_context():
            db.drop_all()
            db.create_all()

    def tearDown(self):
        """Call after every test to remove the created table."""

        with self.app.app_context():
            db.drop_all()
            db.create_all()


class RegisterUserTest(AbstractTest):
    """Illustrate test cases for user registration view."""

    def test_register_null_email(self):
        """Test user registration with null user email
        using post request for RegisterUser class view."""

        user_data = json.dumps({'email': '', 'username': 'cosmas',
                                'first_name': 'first',
                                'last_name': 'last', 'password': 'andela2018',
                                'confirm_password': 'andela2018'})
        response = self.run_app.post('/api/v2/auth/register',
                                     data=user_data, headers=self.headers)

        json_res = json.loads(response.data.decode())
        self.assertEqual(json_res['message'],
                         'Email and Username are required!')

    def test_register_null_username(self):
        """Test user registration with null username
        using post request for RegisterUser class view."""

        user_data = json.dumps({'email': 'test@andela.com',
                                'username': '', 'password': 'andela2018',
                                'confirm_password': 'andela2018'})
        response = self.run_app.post('/api/v2/auth/register',
                                     data=user_data, headers=self.headers)
        json_res = json.loads(response.data.decode())
        self.assertEqual(json_res['message'],
                         'Email and Username are required!')

    def test_register_null_password(self):
        """Test user registration with null password
        using post request for RegisterUser class view."""

        user_data = json.dumps({'email': 'test@andela.com',
                                'username': 'cosmas', 'password': '',
                                'confirm_password': 'andela2018'})
        response = self.run_app.post('/api/v2/auth/register',
                                     data=user_data, headers=self.headers)
        json_res = json.loads(response.data.decode())
        self.assertEqual(json_res['message'],
                         'Password and Confirmation password are required!')

    def test_register_null_confirmation(self):
        """Test user registration with null confirmation password
        using post request for RegisterUser class view."""

        user_data = json.dumps({'email': 'test@andela.com',
                                'username': 'cosmas', 'password': 'andela2018',
                                'confirm_password': ''})
        response = self.run_app.post('/api/v2/auth/register',
                                     data=user_data, headers=self.headers)
        json_res = json.loads(response.data.decode())
        self.assertEqual(json_res['message'],
                         'Password and Confirmation password are required!')

    def test_register_registered_email(self):
        """Test user registration with a registered email
        using post request for RegisterUser class view."""

        first_user = json.dumps({
            'email': 'test@andela.com', 'username': 'testuser',
            'first_name': 'first', 'last_name': 'last',
            'password': 'andela2018', 'confirm_password': 'andela2018'})
        self.run_app.post('/api/v2/auth/register',
                          data=first_user, headers=self.headers)

        second_user = json.dumps({
            'email': 'test@andela.com', 'username': 'cosmas',
            'first_name': 'first', 'last_name': 'last',
            'password': 'andela2018', 'confirm_password': 'andela2018'})
        response = self.run_app.post('/api/v2/auth/register',
                                     data=second_user, headers=self.headers)

        json_res = json.loads(response.data.decode())
        self.assertEqual(json_res['message'], 'User already exists. Sign in!')

    def test_register_registered_name(self):
        """Test user registration with a registered username
        using post request for RegisterUser class view."""

        first_user = json.dumps({
            'email': 'test@andela.com', 'username': 'testuser',
            'first_name': 'first', 'last_name': 'last',
            'password': 'andela2018', 'confirm_password': 'andela2018'})
        self.run_app.post('/api/v2/auth/register',
                          data=first_user, headers=self.headers)

        user_data = json.dumps({'email': 'test2@andela.com',
                                'username': 'testuser', 'first_name': 'first',
                                'last_name': 'last', 'password': 'andela2018',
                                'confirm_password': 'andela2018'})
        response = self.run_app.post('/api/v2/auth/register',
                                     data=user_data, headers=self.headers)

        json_res = json.loads(response.data.decode())
        self.assertEqual(json_res['message'], 'User already exists. Sign in!')

    def test_register_short_password(self):
        """Test user registration with a less than 6 password length
        using post request for RegisterUser class view."""

        user_data = json.dumps({'email': 'test2@andela.com',
                                'username': 'testuser', 'first_name': 'first',
                                'last_name': 'last', 'password': 'a2018',
                                'confirm_password': 'a2018'})
        response = self.run_app.post('/api/v2/auth/register',
                                     data=user_data, headers=self.headers)
        json_res = json.loads(response.data.decode())
        self.assertEqual(json_res['message'],
                         'Password must be more than 6 characters!')

    def test_register_unequal_passwords(self):
        """Test user registration with unequal passwords
        using post request for RegisterUser class view."""

        user_data = json.dumps({'email': 'test2@andela.com',
                                'username': 'testuser', 'first_name': 'first',
                                'last_name': 'last', 'password': 'andela2014',
                                'confirm_password': 'andela2018'})
        response = self.run_app.post('/api/v2/auth/register',
                                     data=user_data, headers=self.headers)
        json_res = json.loads(response.data.decode())
        self.assertEqual(json_res['message'],
                         'Password does not match the confirmation password!')

    def test_register_successful(self):
        """Test user registered successfully with correct data
        using post request for Businesses class view."""

        user_data = json.dumps({'email': 'test2@andela.com',
                                'username': 'testuser', 'first_name': 'first',
                                'last_name': 'last', 'password': 'andela2018',
                                'confirm_password': 'andela2018'})
        response = self.run_app.post('/api/v2/auth/register',
                                     data=user_data, headers=self.headers)
        json_res = json.loads(response.data.decode())
        self.assertEqual(json_res['message'],
                         'You have successfully created an account!')


class LoginUserTest(AbstractTest):
    """Test case for the login api endpoint."""

    def test_login_unregistered_email(self):
        """Test login with unregistered email
        using post request for LoginUser class view."""

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

    def test_login_incorrect_password(self):
        """Test login with an incorrect
        using post request for LoginUser class view."""

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
        self.assertEqual(login_response.status_code, 401)

    def test_login_successful(self):
        """Test login successfully with correct credentials
        using post request for LoginUser class view."""

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
        self.assertEqual(login_response.status_code, 200)
        self.assertTrue(json_res['access_token'])


class LogoutAccessTest(AbstractTest):
    """Test suite for user logout with an access token."""

    def test_logout_successful(self):
        """Test logout successfully using access token
        using post request for UserLogoutAccess class view."""

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
        self.assertEqual(logout_res.status_code, 200)
        self.assertEqual(
            json.loads(logout_res.data.decode())['response_message'],
            'Log out has been successful!')


class LogoutRefreshTest(AbstractTest):
    """Test suite for user logout using a refresh token."""

    def test_logout_successful(self):
        """Test logout successfully using refresh token
        using post request for UserLogoutRefresh class view."""

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
        self.assertEqual(logout_res.status_code, 200)
        self.assertEqual(
            json.loads(logout_res.data.decode())['response_message'],
            'Log out has been successful!')


class ResetPasswordTest(AbstractTest):
    """Test suite for the reset password api endpoint."""

    def test_reset_null_email(self):
        """Test reset password with null registered email
        using post request for ResetPassword class view."""

        self.run_app.post('/api/v2/auth/register',
                          data=self.user_data, headers=self.headers)

        new_data = json.dumps({'email': '', 'password': 'andela2018',
                               'confirm_password': 'andela2018'})
        response = self.run_app.post('/api/v2/auth/reset_password',
                                     data=new_data, headers=self.headers)

        # get the response text in json format
        json_res = json.loads(response.data.decode())
        self.assertEqual(json_res['response_message'], 'Email is required!')

    def test_reset_null_password(self):
        """Test reset password with null new password
        using post request for ResetPassword class view."""

        self.run_app.post('/api/v2/auth/register',
                          data=self.user_data, headers=self.headers)

        new_data = json.dumps({'email': 'test@andela.com', 'password': '',
                               'confirm_password': 'andela2018'})
        response = self.run_app.post('/api/v2/auth/reset_password',
                                     data=new_data, headers=self.headers)

        # get the response text in json format
        json_res = json.loads(response.data.decode())
        self.assertEqual(json_res['response_message'], 'Password is required!')

    def test_reset_null_confirm(self):
        """Test reset password with null password confirmation
        using post request for ResetPassword class view."""

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

    def test_reset_unregistered_email(self):
        """Test reset password with unregistered user email
        using post request for ResetPassword class view."""

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

    def test_reset_password_successful(self):
        """Test reset password successful with correct data
        using post request for ResetPassword class view."""

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
        self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()
