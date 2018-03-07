"""Design test case to test business related endpoints.

This module design test suite into which contains test cases for behaviors that
are expected from API endpoints.

"""



import unittest

from app import app
from src.models.business import Business


class TestBusinessEndpointsTestCase(unittest.TestCase):
    """Illustrate test cases to test expected behavior of business API endpoints. """

    def setUp(self):
        """Enter business records int business records dictionary so that it can be reused by other test cases."""
        self.run_app = app.test_client()
        self.business = Business()
        self.business.create_business(1, 'cosmas', 'Cosma Tech', 'Nairobi', 'Technology', 'Masters of ecommerce')
        self.business.create_business(2, 'Allan', 'Allan Tech', 'Kitale', 'Technology', 'Cryptocurrency')

    def tearDown(self):
        """Delete registered business records after every test case has run."""

        for key in self.business.business_records:
            del self.business.business_records[key]

    def test_view_businesses_endpoint(self):
        """Test whether a get request to business API endpoint has succeeded."""

        response = self.run_app.get('/api/v1/business')
        self.assertEqual(response.status_code, 200)

    def test_view_businesses_by_id_endpoint(self):
        """Test whether providing business id to a get request to business API endpoint has succeeded."""

        response = self.run_app.get('/api/v1/business/1')
        self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()
