import unittest

from app import app
from models import Business

class ConfigTestCase(unittest.TestCase):

    def test_index(self):
        """Ensure flask was set up correctly"""
        run_flask = app.test_client()
        response = run_flask.get('/', content_type='html/text')
        self.assertEqual(response.status_code, 200)


class BusinessTestCase(unittest.TestCase):
    def setUp(self):
        self.business = Business('1', 'cosmas', 'Cosma Tech', 'Nairobi', 'Technology')

    def test_register_business(self):
        self.assertTrue(self.business.create_business())


if __name__ == '__main__':
    unittest.main()
