"""Design test case to test business related functionalities.

This module design test suite in which contains test cases for behaviors that
are expected from business model.

"""


import unittest

from src.models.business import Business


class CreateBusinessTest(unittest.TestCase):

    """Illustrate test cases to test expected behavior of business registration functionality. """

    def setUp(self):
        """Instantiate the Business class so that it can be reused by other test cases."""

        self.business = Business()

    def test_non_integer_business_id_raises_TypeError(self):
        """Test if TypeError is raised when business id not a number."""

        with self.assertRaises(TypeError):
            self.business.create_business('1', 'cosmas', 'Cosma Tech', 'Nairobi', 'Category_one', 'Womens wear')

    def test_negative_integer_business_id_raises_ValueError(self):
        """Test if ValueError is raised when business id a negative number."""

        with self.assertRaises(ValueError):
            self.business.create_business(-1, 'cosmas', 'Cosma Tech', 'Nairobi', 'Category_one', 'Womens wear')

    def test_duplicate_business_id_raises_KeyError(self):
        """Test if KeyError is raised when business id already exist."""

        with self.assertRaises(KeyError):
            self.business.create_business(1, 'cosmas', 'Cosma Tech', 'Nairobi', 'Technology', 'Masters of ecommerce')
            self.business.create_business(1, 'Allan', 'Allan Tech', 'Kitale', 'Technology', 'Cryptocurrency')

    def test_successful_registered_business_returns_successful_message_and_list_of_business_info(self):
        """Test whether a success message is returned when a business is registered."""

        test_result = self.business.create_business(2, 'Bruce', 'Bruce Tech', 'Nairobi', 'Masoko', 'Womens wear')
        self.assertEqual(['Bruce', 'Bruce Tech', 'Nairobi', 'Masoko', 'Womens wear'], test_result["value_list"])
        self.assertEqual("The business is successfully registered!!!", test_result["message"], msg="Fail to register")

if __name__ == '__main__':
    unittest.main()
