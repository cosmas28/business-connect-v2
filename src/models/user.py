"""Demonstrate all user authentication functionalities.

This module provides methods that will enhance the authentication operations
such as user registration, user login, logout, reset password.

"""


class User(object):

    """Illustrate methods to enable user authentication.

    Attributes:
        registered_users (list): A list of dictionaries which store user records.

    """

    def __init__(self):
        self.registered_users = []
        self.user_persistent = {}

    def username_exist(self, username):
        """Check is a username exist.

        Args:
            username (str): username parameter should be unique to identify each user.

        Returns:
           boolean value

        """
        global username_exist
        username_exist = False
        for user in self.registered_users:
            if user["username"] == username:
                username_exist = True

        return username_exist

    def register_user(self, username, password, confirm_password):
        """Register a new user.

        Args:
            username (str): username parameter should be unique to identify each user.
            password (str): password parameter should be at least 6 characters.
            confirm_password (str): confirmation password parameter should match.

        Returns:
            A list of values of the registered username.
            A success message when the user have been registered

        """

        user_data = {
            'username': username,
            'password': password,
        }
        response = ""
        # global username_exist
        # username_exist = False
        # for user in self.registered_users:
        #     if user["username"] == username:
        #         username_exist = True

        if self.username_exist(username):
            response += "The username already exist"
        elif len(username) == 0 and len(password) == 0:
            response += "Username and password is required!"
        elif len(username) == 0 or len(confirm_password) == 0:
            response += "Both username and password is required!"
        elif len(password) < 6:
            response += "Password must be more that 6 characters!"
        elif password != confirm_password:
            response += "The password does not match!"
        else:
            self.registered_users.append(user_data)

        if self.registered_users[-1]["password"] == password:
            response += "Successful registered"

        return response

    def is_user_logged_in(self, username):
        """Login a user.

        Args:
            username (str): username parameter should be unique to identify each user.

        Returns:
            True if the username exist in persistent data

        """
        is_logged_in = False
        if username in self.user_persistent:
            is_logged_in = True

        return is_logged_in

    def login_user(self, username, password):
        """Login a user.

        Args:
            username (str): username parameter should be unique to identify each user.
            password (str): password parameter should be at least 6 characters.

        Returns:
            Successful login

        """

        response = ""

        # global username_exist
        # username_exist = False
        # for user in self.registered_users:
        #     if user["username"] == username:
        #         username_exist = True

        global valid_password
        valid_password = False
        for user in self.registered_users:
            if user["username"] == username and user["password"] == password:
                valid_password = True

        if len(username) == 0 and len(password) == 0:
            response += "Username and password is required!"
        elif len(username) == 0 or len(password) == 0:
            response += "Both username and password is required!"
        elif not self.username_exist(username):
            response += "The username does not exist"
        elif self.is_user_logged_in(username):
            response += "You are already logged in!"
        elif not valid_password:
            response += "The password is invalid!"
        else:
            self.user_persistent[username] = password
            response += "Successful login"

        return response

    def logout_user(self, username):
        """Login a user.

        Args:
            username (str): username parameter should be unique to identify each user.

        Returns:
            Success message

        """

        response = ""
        if username not in self.user_persistent:
            response += "You are already logged out.Please login!"
        elif username in self.user_persistent:
            del self.user_persistent[username]
            response += "Logged out successfully!"

        return response

    def reset_password(self, username, password):
        """Reset use password.

        Args:
            username (str): username parameter should be unique to identify each user.
            password (str): password parameter should be at least 6 characters.

        Returns:
            Success message if the password was changed
            Error message if the username does not exist

        """

        response = ""
        if not self.username_exist(username):
            response += "Invalid username!"
        else:
            for user in self.registered_users:
                if user['username'] == username:
                    user['password'] = password
                    response += "Successful reset password. Login with new password!"

        return response
