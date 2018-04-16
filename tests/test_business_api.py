"""Design test case to test user account related functionalities."""

import unittest

from flask import json
from app.models import db
from app import create_app

# from . import app


class AbstractTest(unittest.TestCase):
    """Define reusable methods and attributes."""

    def setUp(self):
        """Call this before every test."""

        # db.app = app
        # db.create_all()

        self.app = create_app(config_object="testing")
        self.run_app = self.app.test_client()
        self.headers = {
            'Content-type': 'application/json', 'Accept': 'text/plain'}

        with self.app.app_context():
            db.drop_all()
            db.create_all()

    def register_user(self):
        """Register a user."""
        user_data = json.dumps({
            'email': 'test@andela.com', 'username': 'cosmas',
            'first_name': 'first', 'last_name': 'last',
            'password': 'andela2018', 'confirm_password': 'andela2018'})
        return self.run_app.post(
            '/api/v2/auth/register', data=user_data, headers=self.headers)

    def login_user(self):
        """Register a user."""
        login_data = json.dumps({
            'email': 'test@andela.com', 'password': 'andela2018'})

        return self.run_app.post(
            '/api/v2/auth/login', data=login_data, headers=self.headers)

    def authenticate_user(self):
        """Authenticate user and retrieve access token."""
        user_data = json.dumps({
            'email': 'test@andela.com', 'username': 'cosmas',
            'first_name': 'first', 'last_name': 'last',
            'password': 'andela2018', 'confirm_password': 'andela2018'})
        self.run_app.post(
            '/api/v2/auth/register', data=user_data, headers=self.headers)

        login_data = json.dumps({
            'email': 'test@andela.com', 'password': 'andela2018'})

        return self.run_app.post(
            '/api/v2/auth/login', data=login_data, headers=self.headers)

    def register_business(self, access_token):
        """Register a business."""

        business_data = json.dumps({
            'name': 'Palmer Tech', 'category': 'Technology',
            'location': 'Mombasa',
            'summary': 'IoT is transforming human security'})
        return self.run_app.post(
            '/api/v2/businesses', data=business_data,
            headers=dict(Authorization='Bearer ' + access_token))

    def tearDown(self):
        """Call after every test to remove the created table."""

        with self.app.app_context():
            db.drop_all()
            db.create_all()


class CreateBusinessesTest(AbstractTest):
    """Test suite for business registration functionality."""

    def test_registration_null_name(self):
        """Test business registration with null business name
        using post request for Businesses class view."""

        access_token = json.loads(
            self.authenticate_user().data.decode())['access_token']

        business_data = json.dumps({
            'name': '', 'category': 'Technology', 'location': 'Nairobi',
            'summary': 'AI is transforming human life'})

        response = self.run_app.post(
            '/api/v2/businesses', data=business_data,
            headers=dict(Authorization='Bearer ' + access_token))

        self.assertEqual(response.status_code, 406)

    def test_registration_null_category(self):
        """Test business registration with null business category
        using post request for Businesses class view."""
        access_token = json.loads(
            self.authenticate_user().data.decode())['access_token']

        business_data = json.dumps({
            'name': 'Cosmas Tech', 'category': '', 'location': 'Nairobi',
            'summary': 'AI is transforming human life'})

        response = self.run_app.post(
            '/api/v2/businesses', data=business_data,
            headers=dict(Authorization='Bearer ' + access_token))

        self.assertEqual(response.status_code, 406)

    def test_registration_null_location(self):
        """Test business registration with null business location
        using post request for Businesses class view."""
        access_token = json.loads(
            self.authenticate_user().data.decode())['access_token']

        business_data = json.dumps({
            'name': 'Cosmas Tech', 'category': 'Technology', 'location': '',
            'summary': 'AI is transforming human life'})

        response = self.run_app.post(
            '/api/v2/businesses', data=business_data,
            headers=dict(Authorization='Bearer ' + access_token))

        self.assertEqual(response.status_code, 406)

    def test_registration_null_summary(self):
        """Test business registration with null business summary
        using post request for Businesses class view."""
        access_token = json.loads(
            self.authenticate_user().data.decode())['access_token']

        business_data = json.dumps({
            'name': 'Cosmas Tech', 'category': 'Technology',
            'location': 'Nairobi', 'summary': ''})

        response = self.run_app.post(
            '/api/v2/businesses', data=business_data,
            headers=dict(Authorization='Bearer ' + access_token))

        self.assertEqual(response.status_code, 406)

    def test_registration_unique_name(self):
        """Test business registration with unique name
        using post request for Businesses class view."""
        access_token = json.loads(
            self.authenticate_user().data.decode())['access_token']

        first_business_data = json.dumps({
            'name': 'CosmasTech', 'category': 'Technology',
            'location': 'Nairobi', 'summary': 'AI is transforming human life'})

        self.run_app.post(
            '/api/v2/businesses', data=first_business_data,
            headers=dict(Authorization='Bearer ' + access_token))

        business_data = json.dumps({
            'name': 'CosmasTech', 'category': 'Technology',
            'location': 'Mombasa',
            'summary': 'IoT is transforming human security'})

        response = self.run_app.post(
            '/api/v2/businesses', data=business_data,
            headers=dict(Authorization='Bearer ' + access_token))

        self.assertEqual(
            json.loads(response.data.decode())['response_message'],
            'Business name already registered!')

    def test_registration_successful(self):
        """Test business registered successfully with correct data
        using post request for Businesses class view."""
        access_token = json.loads(
            self.authenticate_user().data.decode())['access_token']
        response = self.register_business(access_token)

        self.assertEqual(
            json.loads(response.data.decode())['response_message'],
            'Business has been registered successfully!')

    def test_view_all_businesses(self):
        """Test view all registered businesses
        using get request for Businesses class view."""
        access_token = json.loads(
            self.authenticate_user().data.decode())['access_token']
        self.register_business(access_token)

        response = self.run_app.get(
            '/api/v2/businesses',
            headers=dict(Authorization='Bearer ' + access_token))

        self.assertIn('Palmer Tech', str(response.data))


class ViewBusinessTest(AbstractTest):
    """Test cases for viewing one business by business id."""

    def test_view_unregistered(self):
        """Test view unregistered business
        using get request for OneBusinesses class view."""
        access_token = json.loads(
            self.authenticate_user().data.decode())['access_token']
        self.register_business(access_token)

        response = self.run_app.get(
            '/api/v2/businesses/4',
            headers=dict(Authorization='Bearer ' + access_token))

        self.assertEqual(response.status_code, 404)

    def test_view_successful(self):
        """Test view a registered business successfully
        using get request for OneBusiness class view."""
        access_token = json.loads(
            self.authenticate_user().data.decode())['access_token']
        self.register_business(access_token)

        response = self.run_app.get(
            '/api/v2/businesses/1',
            headers=dict(Authorization='Bearer ' + access_token))

        self.assertIn('Palmer Tech', str(response.data))


class UpdateBusinessTest(AbstractTest):
    """Test cases for updating a business."""

    def test_update_unregistered(self):
        """Test update unregistered business
        using put request for OneBusiness class view."""
        access_token = json.loads(
            self.authenticate_user().data.decode())['access_token']
        self.register_business(access_token)

        new_data = json.dumps({
            'name': 'Palmer Tech', 'category': 'Technology',
            'location': 'Nairobi',
            'summary': 'IoT is transforming human security'})
        response = self.run_app.put(
            '/api/v2/businesses/3', data=new_data,
            headers=dict(Authorization='Bearer ' + access_token))

        self.assertEqual(response.status_code, 404)

    def test_update_successful(self):
        """Test update registered business successfully
        using put request for OneBusiness class view."""
        access_token = json.loads(
            self.authenticate_user().data.decode())['access_token']
        self.register_business(access_token)

        new_data = json.dumps({
            'name': 'Palmer Tech', 'category': 'Technology',
            'location': 'Nairobi',
            'summary': 'IoT is transforming human security'})
        response = self.run_app.put(
            '/api/v2/businesses/1', data=new_data,
            headers=dict(Authorization='Bearer ' + access_token))

        self.assertIn('Nairobi', str(response.data))


class DeleteBusinessTest(AbstractTest):
    """Test cases for deleting a business."""

    def test_delete_unregistered(self):
        """Test delete unregistered business
        using delete request for OneBusiness class view."""
        access_token = json.loads(
            self.authenticate_user().data.decode())['access_token']
        self.register_business(access_token)

        response = self.run_app.delete(
            '/api/v2/businesses/5',
            headers=dict(Authorization='Bearer ' + access_token))

        self.assertEqual(response.status_code, 404)

    def test_delete_successful(self):
        """Test delete successfully
        using delete request for OneBusiness class view."""
        access_token = json.loads(
            self.authenticate_user().data.decode())['access_token']
        self.register_business(access_token)

        response = self.run_app.delete(
            '/api/v2/businesses/1',
            headers=dict(Authorization='Bearer ' + access_token))

        self.assertEqual(
            json.loads(response.data.decode())['response_message'],
            'Business has been deleted successfully!')


class BusinessCategoryTest(AbstractTest):
    """Test suite for testing filtering business by category."""

    def test_filter_null_category(self):
        """Test filter businesses in unregistered category
        using query string in BusinessCategory class view."""
        access_token = json.loads(
            self.authenticate_user().data.decode())['access_token']
        self.register_business(access_token)

        response = self.run_app.get(
            '/api/v2/businesses/category?q=Accounting&start=1&limit=2',
            headers=dict(Authorization='Bearer ' + access_token))

        json_res = json.loads(response.data.decode())
        self.assertEqual(json_res['response_message'],
                         'Businesses not found is this category!')

    def test_filter_successful(self):
        """Test filter businesses by category
        using query string in BusinessCategory class view."""
        access_token = json.loads(
            self.authenticate_user().data.decode())['access_token']
        self.register_business(access_token)

        response = self.run_app.get(
            '/api/v2/businesses/category?q=Technology&start=1&limit=2',
            headers=dict(Authorization='Bearer ' + access_token))

        self.assertIn('Palmer Tech', str(response.data))


class BusinessLocationTest(AbstractTest):
    """Test suite for testing filtering business by category."""

    def test_filter_null_location(self):
        """Test filter businesses in unregistered location
        using query string in BusinessLocation class view."""
        access_token = json.loads(
            self.authenticate_user().data.decode())['access_token']
        self.register_business(access_token)

        response = self.run_app.get(
            '/api/v2/businesses/location?q=kitale&start=1&limit=2',
            headers=dict(Authorization='Bearer ' + access_token))

        json_res = json.loads(response.data.decode())
        self.assertEqual(json_res['response_message'],
                         'Businesses not found in this location!')

    def test_filter_successful(self):
        """Test filter businesses in by location successfully
        using query string in BusinessLocation class view."""
        access_token = json.loads(
            self.authenticate_user().data.decode())['access_token']
        self.register_business(access_token)

        response = self.run_app.get(
            '/api/v2/businesses/location?q=Mombasa&start=1&limit=2',
            headers=dict(Authorization='Bearer ' + access_token))

        self.assertIn('Palmer Tech', str(response.data))


class BusinessSearchTest(AbstractTest):
    """Test suite for testing business search."""

    def test_search_unregistered(self):
        """Test search unregistered business
        using query string in SearchBusiness class view."""
        access_token = json.loads(
            self.authenticate_user().data.decode())['access_token']
        self.register_business(access_token)

        response = self.run_app.get(
            '/api/v2/businesses/search?q=katel&start=1&limit=2',
            headers=dict(Authorization='Bearer ' + access_token))

        json_res = json.loads(response.data.decode())
        self.assertEqual(json_res['response_message'], 'Business not found!')

    def test_search_registered(self):
        """Test search registered business
        using query string in SearchBusiness class view."""
        access_token = json.loads(
            self.authenticate_user().data.decode())['access_token']
        self.register_business(access_token)

        response = self.run_app.get(
            '/api/v2/businesses/search?q=Palmer&start=1&limit=2',
            headers=dict(Authorization='Bearer ' + access_token))

        self.assertIn('Palmer Tech', str(response.data))

    def test_pagination_api(self):
        """Test business results pagination
        using query string in SearchBusiness class view."""
        access_token = json.loads(
            self.authenticate_user().data.decode())['access_token']

        self.register_business(access_token)
        second_business = json.dumps({
            'name': 'TechBusiness', 'category': 'Technology',
            'location': 'Nairobi',
            'summary': 'A network of different businesses'})
        self.run_app.post(
            '/api/v2/businesses', data=second_business,
            headers=dict(Authorization='Bearer ' + access_token))
        third_business = json.dumps({
            'name': 'TechSchool', 'category': 'Technology',
            'location': 'Dar es Salaam',
            'summary': 'A network students across the world.'})
        self.run_app.post(
            '/api/v2/businesses', data=third_business,
            headers=dict(Authorization='Bearer ' + access_token))

        response = self.run_app.get(
            '/api/v2/businesses/search?q=Tech&start=1&limit=2',
            headers=dict(Authorization='Bearer ' + access_token))

        self.assertEqual(
            len(json.loads(response.data.decode()).get('business_list')), 2)


if __name__ == '__main__':
    unittest.main()
