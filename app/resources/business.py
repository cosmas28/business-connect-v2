"""Demonstrate all business related API endpoints.

This module provides API endpoints to register business, view a single business, view all
businesses.

"""

from flask import Blueprint, abort, request, make_response, jsonify

from flask_restful import (Resource, Api, reqparse)
from flask_jwt_extended import jwt_required

from app.models.user import Business
from app.models import db


def business_name_registered(name):
    """Check whether the business is already registered.

    Args:
        name(str): Unique business name.

    Returns:
        Boolean value.
    """

    registered = Business.query.filter_by(name=name).first()

    if registered:
        return True


class Businesses(Resource):

    """Illustrate API endpoints to register and view businesses."""

    @jwt_required
    def post(self):
        """Register a business.

        Returns:
            A success message to indicate successful registration.

        Raises:
            Error message when business name is empty.
            Error message when business category is empty.
            Error message when business location is empty.
            Error message when business summary is empty.
            Error message when business name is already registered.

        """
        req_data = request.get_json(force=True)
        business_name = req_data['name']
        business_category = req_data['category']
        business_location = req_data['location']
        business_summary = req_data['summary']

        try:

            if len(business_name) == 0:
                response = {
                    'response_message': 'Business name is required!'
                }
                return make_response(jsonify(response))
            elif len(business_category) == 0:
                response = {
                    'response_message': 'Business category is required!'
                }
                return make_response(jsonify(response))
            elif len(business_location) == 0:
                response = {
                    'response_message': 'Business location is required!'
                }
                return make_response(jsonify(response))
            elif len(business_summary) == 0:
                response = {
                    'response_message': 'Business summary is required!'
                }
                return make_response(jsonify(response))
            elif business_name_registered(business_name):
                response = {
                    'response_message': 'Business name already registered!'
                }
                return make_response(jsonify(response))
            else:
                business = Business(business_name, business_category, business_location, business_summary)
                db.session.add(business)
                db.session.commit()

                response = {
                    'response_message': 'Business has been registered successfully!',
                    'status_code': 201
                }

                return make_response(jsonify(response))

        except Exception as e:
            response = {
                'response_message': str(e)
            }

            return make_response(jsonify(response))

    def get(self):
        """View all registered businesses.

        Returns:
            A json format records of the registered businesses.

        """

        business_dict = business.view_all_businesses()
        return business_dict, 200


class OneBusinessRecord(Resource):

    """Illustrate API endpoints to manipulate business data.

       Attributes:
           business (class): A class that implement business related methods.

       """

    def get(self, business_id):
        """View a registered business by id.

        Returns:
            A json record of the registered business.

        """
        response = business.view_business_by_id(business_id)

        if response.get('message') == 'There is no registered business!':
            return 'Business does not exist', abort(404)

        return response, 200

    def put(self, business_id):
        """Update a registered businesses.

        Args:
            business_id (int): business id parameter should be unique to identify each business.

        Returns:
           A successful message when the business record is deleted.

        """

        req_data = request.get_json()
        business_owner = req_data['business_owner']
        business_name = req_data['business_name']
        business_category = req_data['business_category']
        business_location = req_data['business_location']
        business_summary = req_data['business_summary']

        response = business.update_business(business_id, business_owner, business_name, business_category,
                                            business_location, business_summary)

        return response, 200

    def delete(self, business_id):
        """Delete a registered businesses.

        Args:
            business_id (int): business id parameter should be unique to identify each business.

        Returns:
           A successful message when the business record is deleted.

        """

        response = business.delete_business(business_id)

        return response, 200


business_api = Blueprint('resources.business', __name__)
api = Api(business_api)
api.add_resource(
    Businesses,
    '/businesses',
    endpoint='businesses'
)
# api.add_resource(
#     OneBusinessRecord,
#     '/businesses/<int:business_id>',
#     endpoint='businesses'
# )
