"""Design test case to test user account related functionalities.

This module design test suite in which contains test cases for behaviors that
are expected from user model.

"""


import unittest

from src.models.user import User


class AbstractTest(unittest.TestCase):

    """Illustrate test cases to test expected behavior of business registration functionality. """

    def setUp(self):
        """Instantiate the User class so that it can be reused by other test cases."""

        self.user = User()
        self.user.register_user("cosmas28", "password123", "password123")


class UserRegistrationTest(AbstractTest):

    """Illustrate test cases to test expected behavior of business registration functionality. """

    # def tearDown(self):
    #     self.user.registered_users.remove(0)

    def test_empty_user_input(self):
        """Test user inserted no data."""

        self.assertEqual(self.user.register_user("", "", ""), "Username and password is required!")

    def test_duplicate_username(self):
        """Test username already exist."""

        test_resonse = self.user.register_user("cosmas28", "mark123444", "mark123444")
        self.assertEqual(test_resonse, "The username already exist")

    def test_password_length(self):
        """Test user password to be more than 6 characters."""

        test_response = self.user.register_user("facebook", "net23", "net23")
        self.assertEqual(test_response, "Password must be more that 6 characters!")

    def test_password_confirmation(self):
        """Test user password match confirmation password."""

        test_response = self.user.register_user("facebook", "passion123", "passion1")
        self.assertEqual(test_response, "The password does not match!")

    def test_one_user_input_missing(self):
        """Test user input one field."""

        self.assertEqual(self.user.register_user("yoyo2018", "TIA2018", ""), "Both username and password is required!")
        self.assertEqual(self.user.register_user("", "TIA2018", "TIA2018"), "Both username and password is required!")

    def test_success_user_registration(self):
        """Test user registration is successful."""

        test_response = self.user.register_user("augustino28", "andela2018", "andela2018")
        self.assertEqual(test_response, "Successful registered")
        # self.assertIn("augustino28", test_response["user_list"])


class UserLoginTest(AbstractTest):

    """Illustrate test cases to test expected behavior of user login functionality. """

    def test_empty_user_input_when_login(self):
        """Test user inserted no data when login."""

        self.assertEqual(self.user.login_user("", ""), "Username and password is required!")

    def test_one_user_input_missing_when_login(self):
        """Test user input one login parameter."""

        self.assertEqual(self.user.login_user("yoyo2018", ""), "Both username and password is required!")
        self.assertEqual(self.user.login_user("", "TIA2018"), "Both username and password is required!")

    def test_user_login_successfully(self):
        """Test can login successfully."""

        # self.assertTrue(self.user.login_user)
        test_response = self.user.login_user("cosmas28", "password123")
        self.assertEqual(test_response, "Successful login")

    def test_user_already_logged_in(self):
        """Test whether user is already logged in."""

        self.user.login_user("cosmas28", "password123")
        test_response = self.user.is_user_logged_in("cosmas28")
        self.assertTrue(test_response)


if __name__ == '__main__':
    unittest.main()
