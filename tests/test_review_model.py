"""Design test case to test business review related functionalities.

This module design test suite in which contains test cases for behaviors that
are expected from review model.

"""


import unittest

from app import business
from app.models.reviews import Reviews


class AddReviewTest(unittest.TestCase):

    """Illustrate test cases to test expected behavior of add reviews functionality. """

    def setUp(self):
        """Instantiate the Review class so that it can be reused by other test cases."""

        self.reviews = Reviews()
        business.create_business(1, 'Cosmas', 'Cosma Tech', 'Nairobi', 'Technology', 'Masters of ecommerce')

    def tearDown(self):
        """Delete registered business records after every test case has run."""

        del business.business_records[1]

    def test_empty_business_id(self):
        """Test whether business id is empty."""

        self.assertEqual(self.reviews.add_review('', 'first review', '16-03-107'), 'Business id is required!')

    def test_business_id_existence(self):
        """Test if a KeyError will be raised when the business id does not exist."""

        with self.assertRaises(KeyError):
            self.reviews.add_review(2, 'first review', '16-03-107')

    def test_empty_business_review(self):
        """Test whether business review field is empty."""

        self.assertEqual(self.reviews.add_review(1, '', '16-03-107'), 'Business review was not provided!')

    def test_business_review_added_successfully(self):
        """Test whether business review was successfully added."""

        self.assertEqual(self.reviews.add_review(1, 'first review', '16-03-107'), 'Business review added successfully!')


if __name__ == '__main__':
    unittest.main()
