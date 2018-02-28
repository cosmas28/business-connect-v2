import unittest

from app import app


class ConfigTestCase(unittest.TestCase):

    def test_index(self):
        """Ensure flask was set up correctly"""
        run_flask = app.test_client()
        response = run_flask.get('/', content_type='html/text')
        self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()
