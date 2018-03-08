"""Demonstrate all business related API endpoints.

This module provides API endpoints to register business, view a single business, view all
businesses.

"""

from flask import Blueprint, abort, request

from flask.ext.restful import (Resource, Api, reqparse)

from app.models.business import Business


business = Business()


class BusinessRecord(Resource):

    """Illustrate API endpoints to register and view business.

    Attributes:
        reqparse (object): A request parsing interface designed to access simple and uniform
        variables on the flask.request object.

    """

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('business_id',
                                   required=True,
                                   help='Business id is required',
                                   location=['form', 'json']
                                    )
        self.reqparse.add_argument('business_owner',
                                   required=True,
                                   help='Business owner is required',
                                   location=['form', 'json'])
        self.reqparse.add_argument('business_name',
                                   required=True,
                                   help='Business name is required',
                                   location=['form', 'json'])
        self.reqparse.add_argument('business_category',
                                   required=True,
                                   help='Business category is required',
                                   location=['form', 'json'])
        self.reqparse.add_argument('business_location',
                                   required=True,
                                   help='Business location is required',
                                   location=['form', 'json'])
        self.reqparse.add_argument('business_summary',
                                   required=True,
                                   help='Business summary is required',
                                   location=['form', 'json'])

    def post(self):
        """Register a business.

        Returns:
            A success message to indicate successful registration.

        Raises:
            TypeError is raised when business id not a number.
            ValueError is raised when business id a negative number.
            KeyError is raised when business id already exist.
            Error message when no data supplied.

        """
        req_data = request.get_json()
        business_id = req_data['business_id']
        business_owner = req_data['business_owner']
        business_name = req_data['business_name']
        business_category = req_data['business_category']
        business_location = req_data['business_location']
        business_summary = req_data['business_summary']

        save_result = business.create_business(business_id, business_owner, business_name, business_category,
                                               business_location, business_summary)
        return save_result["message"], 201

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


business_api = Blueprint('resources.business', __name__)
api = Api(business_api)
api.add_resource(
    BusinessRecord,
    '/business',
    endpoint='business'
)
api.add_resource(
    OneBusinessRecord,
    '/businesses/<int:business_id>',
    endpoint='businesses'
)
