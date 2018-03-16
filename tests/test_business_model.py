"""Design test case to test business related functionalities.

This module design test suite in which contains test cases for behaviors that
are expected from business model.

"""


import unittest

from app.models.business import Business


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

    def test_successful_registered_business(self):
        """Test whether a success message is returned when a business is registered."""

        test_result = self.business.create_business(2, 'Bruce', 'Bruce Tech', 'Nairobi', 'Masoko', 'Womens wear')
        self.assertEqual(['Bruce', 'Bruce Tech', 'Nairobi', 'Masoko', 'Womens wear'], test_result["value_list"])
        self.assertEqual('The business is successfully registered!!!', test_result['message'], msg='Fail to register')


class ViewBusinessTest(unittest.TestCase):

    """Illustrate test cases to test expected behavior of view registered functionality. """

    def setUp(self):
        """Instantiate the Business class so that it can be reused by other test cases."""

        self.business = Business()

    def test_view_all_businesses_records(self):
        """Test whether a dictionary of all the registered businesses will be returned."""

        self.business.create_business(1, 'Cosmas', 'Cosma Tech', 'Nairobi', 'Technology', 'Masters of ecommerce')
        self.business.create_business(2, 'Allan', 'Allan Tech', 'Kitale', 'Technology', 'Cryptocurrency')
        self.assertEqual(
            self.business.view_all_businesses(), {1: {'owner': 'Cosmas', 'name': 'Cosma Tech', 'location': 'Nairobi',
                                                      'category': 'Technology', 'summary': 'Masters of ecommerce'},
                                                  2: {'owner': 'Allan', 'name': 'Allan Tech', 'location': 'Kitale',
                                                      'category': 'Technology', 'summary': 'Cryptocurrency'}}
        )

    def test_view_business_by_id(self):
        """Test whether a dictionary of the registered information will be returned."""

        self.business.create_business(1, 'Cosmas', 'Cosma Tech', 'Nairobi', 'Technology', 'Masters of ecommerce')
        self.assertEqual(
            self.business.view_business_by_id(1), {'owner': 'Cosmas', 'name': 'Cosma Tech', 'location': 'Nairobi',
                                                 'category': 'Technology', 'summary': 'Masters of ecommerce'}
        )

    def test_view_by_category(self):
        """Test whether a dictionary of all the business with the same category will be returned."""

        self.business.create_business(1, 'Cosmas', 'Cosma Tech', 'Nairobi', 'Technology', 'Masters of ecommerce')
        self.business.create_business(2, 'Allan', 'Allan Tech', 'Kitale', 'Technology', 'Cryptocurrency')
        self.business.create_business(3, 'John', 'John Corporate', 'Kisumu', 'Fishing', 'Process fish')
        self.assertEqual(
            self.business.view_businesses_by_category(),
                {1: {'owner': 'Cosmas', 'name': 'Cosma Tech', 'location': 'Nairobi',
                    'category': 'Technology', 'summary': 'Masters of ecommerce'},
                  2: {'owner': 'Allan', 'name': 'Allan Tech', 'location': 'Kitale',
                      'category': 'Technology', 'summary': 'Cryptocurrency'}}
        )

    def test_view_by_location(self):
        """Test whether a dictionary of all the business in the same location will be returned."""

        self.business.create_business(1, 'Cosmas', 'Cosma Tech', 'Nairobi', 'Technology', 'Masters of ecommerce')
        self.business.create_business(2, 'John', 'John Corporate', 'Kitale', 'Fishing', 'Process fish')
        self.business.create_business(3, 'Allan', 'Allan Tech', 'Kitale', 'Technology', 'Cryptocurrency')
        self.assertEqual(
            self.business.view_businesses_by_location(),
            {2: {'owner': 'John', 'name': 'John Corporate', 'location': 'Kitale',
                 'category': 'Fishing', 'summary': 'Process fish'},
             3: {'owner': 'Allan', 'name': 'Allan Tech', 'location': 'Kitale',
                 'category': 'Technology', 'summary': 'Cryptocurrency'}}
        )

    def test_non_existed_business_id_raises_KeyError(self):
        """Test if a KeyError will be raised when the business id does not exist."""

        self.business.create_business(1, 'Cosmas', 'Cosma Tech', 'Nairobi', 'Technology', 'Masters of ecommerce')
        self.business.create_business(2, 'John', 'John Corporate', 'Kitale', 'Fishing', 'Process fish')
        self.business.create_business(3, 'Allan', 'Allan Tech', 'Kitale', 'Technology', 'Cryptocurrency')
        with self.assertRaises(KeyError):
            self.business.view_business_by_id(4)

    def test_non_existed_business_category_print_not_found(self):
        """Test whether a not found message will be returned if no business is located in the given location."""

        self.business.create_business(1, 'Cosmas', 'Cosma Tech', 'Nairobi', 'Technology', 'Masters of ecommerce')
        self.business.create_business(2, 'John', 'John Corporate', 'Kitale', 'Fishing', 'Process fish')
        self.business.create_business(3, 'Allan', 'Allan Tech', 'Kitale', 'Technology', 'Cryptocurrency')
        self.assertEqual('Not found', self.business.view_business_by_category('Accounting'))

    def test_non_existed_business_location_print_not_found(self):
        """Test whether a not found message will be returned if no business is related to the given category."""

        self.business.create_business(1, 'Cosmas', 'Cosma Tech', 'Nairobi', 'Technology', 'Masters of ecommerce')
        self.business.create_business(2, 'John', 'John Corporate', 'Kitale', 'Fishing', 'Process fish')
        self.business.create_business(3, 'Allan', 'Allan Tech', 'Kitale', 'Technology', 'Cryptocurrency')
        self.assertEqual('Not found', self.business.view_business_by_location('Mombassa'))


class DeleteBusinessTest(unittest.TestCase):
    """Illustrate test cases to test expected behavior of delete business functionality. """

    def setUp(self):
        """Instantiate the Business class so that it can be reused by other test cases."""

        self.business = Business()

    def test_business_id_existence(self):
        """Test if a KeyError will be raised when the business id does not exist."""

        self.business.create_business(1, 'Cosmas', 'Cosma Tech', 'Nairobi', 'Technology', 'Masters of ecommerce')
        self.business.create_business(2, 'John', 'John Corporate', 'Kitale', 'Fishing', 'Process fish')
        with self.assertRaises(KeyError):
            self.business.delete_business(4)

    def test_empty_business_id(self):
        """Test whether no business id is provided."""

        self.assertEqual(self.business.delete_business(''), 'Business is required!')

    def test_negative_integer_business_id_raises_ValueError(self):
        """Test if ValueError is raised when business id a negative number."""

        with self.assertRaises(ValueError):
            self.business.delete_business(-1)

    def test_non_integer_business_id_raises_TypeError(self):
        """Test if TypeError is raised when business id not a number."""

        with self.assertRaises(TypeError):
            self.business.delete_business('1')


class UpdateBusinessTest(unittest.TestCase):
    """Illustrate test cases to test expected behavior of update business functionality. """

    def setUp(self):
        """Instantiate the Business class so that it can be reused by other test cases."""

        self.business = Business()
        self.business.create_business(1, 'Cosmas', 'Cosma Tech', 'Nairobi', 'Technology', 'Masters of ecommerce')
        self.business.create_business(2, 'John', 'John Corporate', 'Kitale', 'Fishing', 'Process fish')

    def test_business_id_existence(self):
        """Test if a KeyError will be raised when the business id does not exist."""

        # self.business.create_business(1, 'Cosmas', 'Cosma Tech', 'Nairobi', 'Technology', 'Masters of ecommerce')
        # self.business.create_business(2, 'John', 'John Corporate', 'Kitale', 'Fishing', 'Process fish')
        with self.assertRaises(KeyError):
            self.business.update_business(3, 'Cosmas', 'Cosma Tech', 'Nairobi', 'Technology',
                                          'Masters of ecommerce and statics')

    def test_empty_business_id(self):
        """Test whether no business id is provided."""

        self.assertEqual(self.business.update_business('', 'Cosmas', 'Cosma Tech', 'Nairobi', 'Technology',
                                                       'Masters of ecommerce and statics'), 'Business id is required!')

    def test_negative_integer_business_id_raises_ValueError(self):
        """Test if ValueError is raised when business id a negative number."""

        with self.assertRaises(ValueError):
            self.business.update_business(-1, 'Cosmas', 'Cosma Tech', 'Nairobi', 'Technology',
                                          'Masters of ecommerce and statics')

    def test_non_integer_business_id_raises_TypeError(self):
        """Test if TypeError is raised when business id not a number."""

        with self.assertRaises(TypeError):
            self.business.update_business('1', 'Cosmas', 'Cosma Tech', 'Nairobi', 'Technology',
                                          'Masters of ecommerce and statics')

    def test_business_updated_successfully(self):
        """Test whether business was updated successfully."""

        response = self.business.update_business(1, 'Cosmas', 'Cosma Tech', 'Nairobi', 'Technology',
                                                 'Masters of ecommerce and statics')
        self.assertEqual(response, "Business was successfully updated!")


if __name__ == '__main__':
    unittest.main()
