"""Design test case to test user account related functionalities.

This module design test suite in which contains test cases for behaviors that
are expected from user model.

"""


import unittest

from . import app
from app.models.user import db, User


class AbstractTest(unittest.TestCase):

    def setUp(self):
        """Call this before every test."""

        db.app = app
        db.create_all()

    def tearDown(self):
        """Call after every test to remove the created table."""

        db.session.remove()
        db.drop_all()


class UserModelTest(AbstractTest):

    """Illustrate test cases to test expected behavior of user registration functionality. """

    def test_user_model_can_register_users(self):
        """Test whether user model can register users."""

        user = User('test@andela.com', 'testuser', 'first', 'last', 'password')
        db.session.add(user)
        db.session.commit()
        self.assertEqual(User.query.count(), 1)

    def test_user_password(self):
        """Test whether user password matches hashed password."""

        user = User('test@andela.com', 'testuser', 'first', 'last', 'password')
        db.session.add(user)
        db.session.commit()

        self.assertTrue(user.check_password('password'))

    # def test_empty_username(self):
    #     """Test empty username."""
    #
    #     self.assertEqual(self.user.register_user('test2@andela.com', '', 'first', 'last', 'password', 'password'),
    #                      'Username is required!')
    #
    # def test_empty_firstname(self):
    #     """Test empty first name."""
    #
    #     self.assertEqual(self.user.register_user('test2@andela.com', 'testuser2', '', 'last', 'password', 'password'),
    #                      'First name is required!')
    #
    # def test_empty_lastname(self):
    #     """Test empty user last name."""
    #
    #     self.assertEqual(self.user.register_user('test2@andela.com', 'testuser2', 'first', '', 'password', 'password'),
    #                      'Last name is required!')
    #
    # def test_empty_password(self):
    #     """Test empty password."""
    #
    #     self.assertEqual(self.user.register_user('test2@andela.com', 'testuser2', 'first', 'last', '', 'password'),
    #                      'Password is required!')
    #
    # def test_empty_confirm_password(self):
    #     """Test empty password confirmation."""
    #
    #     self.assertEqual(self.user.register_user('test2@andela.com', 'testuser2', 'first', 'last', 'password', ''),
    #                      'Confirmation password is required!')
    #
    # def test_duplicate_email(self):
    #     """Test whether the email address exist."""
    #
    #     test_response = self.user.register_user('test@andela.com', 'testuser2', 'first', 'last', 'password', 'password')
    #     self.assertEqual(test_response, 'The email address already exist!')
    #
    # def test_duplicate_username(self):
    #     """Test username already exist."""
    #
    #     test_response = self.user.register_user('test@andela.com', 'testuser', 'first', 'last', 'password', 'password')
    #     self.assertEqual(test_response, 'The username already exist!')
    #
    # def test_password_length(self):
    #     """Test user password to be more than 6 characters."""
    #
    #     test_response = self.user.register_user('test2@andela.com', 'testuser2', 'first', 'last', 'passd',
    #                                             'passd')
    #     self.assertEqual(test_response, 'Password must be more than 6 characters!')
    #
    # def test_password_confirmation(self):
    #     """Test user password match confirmation password."""
    #
    #     test_response = self.user.register_user('test2@andela.com', 'testuser2', 'first', 'last', 'password',
    #                                             'passwod')
    #     self.assertEqual(test_response, 'The password does not match!')
    #
    # def test_success_user_registration(self):
    #     """Test user registration is successful."""
    #
    #     test_response = self.user.register_user('test2@andela.com', 'testuser2', 'first', 'last', 'password',
    #                                             'password')
    #     self.assertEqual(test_response, 'You are successful registered')


# class UserLoginTest(AbstractTest):
#
#     """Illustrate test cases to test expected behavior of user login functionality. """
#
#     def test_empty_user_input_when_login(self):
#         """Test user inserted no data when login."""
#
#         self.assertEqual(self.user.login_user('', ''), 'Username and password is required!')
#
#     def test_one_user_input_missing_when_login(self):
#         """Test user input one login parameter."""
#
#         self.assertEqual(self.user.login_user('yoyo2018', ''), 'Both username and password is required!')
#         self.assertEqual(self.user.login_user('', 'TIA2018'), 'Both username and password is required!')
#
#     def test_user_login_successfully(self):
#         """Test can login successfully."""
#
#         # self.assertTrue(self.user.login_user)
#         test_response = self.user.login_user('cosmas28', 'password123')
#         self.assertEqual(test_response, 'Successful login')
#
#     def test_user_already_logged_in(self):
#         """Test whether user is already logged in."""
#
#         self.user.login_user('cosmas28', 'password123')
#         test_response = self.user.is_user_logged_in('cosmas28')
#         self.assertTrue(test_response)
#
#     def test_logout_user(self):
#         """Test whether user can log out."""
#
#         self.user.login_user('cosmas28', 'password123')
#         test_response = self.user.logout_user('cosmas28')
#         self.assertEqual(test_response, 'Logged out successfully!')
#
#     def test_user_already_logged_out(self):
#         """Test user cannot log out twice."""
#
#         self.user.login_user('cosmas28', 'password123')
#         self.user.logout_user('cosmas28')
#         test_response = self.user.logout_user('cosmas28')
#         self.assertEqual(test_response, 'You are already logged out.Please login!')
#
#     def test_user_can_reset_password(self):
#         """Test user can reset their passwords."""
#
#         test_response = self.user.reset_password('cosmas28', 'newpassword')
#         self.assertEqual(test_response, 'Successful reset password. Login with new password!')
#
#     def test_reset_password_with_wrong_username(self):
#         """Test user can reset their passwords."""
#
#         test_response = self.user.reset_password('cosmas', 'newpassword')
#         self.assertEqual(test_response, 'Invalid username!')


if __name__ == '__main__':
    unittest.main()
